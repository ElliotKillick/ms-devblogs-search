#!/usr/bin/python3

# Copyright (C) 2024 Elliot Killick <contact@elliotkillick.com>
# Licensed under the MIT License. See LICENSE file for details.

from pathlib import Path
import os
import re
import requests
from lxml import etree

PROGRAM_DIRECTORY = Path(__file__).parent.resolve()

# Configuration variables
# Right now, we're specifically searching for Old New Thing articles
# We append a page number to this base URL
PAGE_LISTING_BASE_URL = "https://devblogs.microsoft.com/oldnewthing/page/"
OUTPUT_DIRECTORY = PROGRAM_DIRECTORY / "out"

os.mkdir(OUTPUT_DIRECTORY)
os.mkdir(f"{OUTPUT_DIRECTORY}/articles")
os.mkdir(f"{OUTPUT_DIRECTORY}/comments")

# Server may block Python Requests user-agent so report as curl instead
HEADERS = {
    'User-Agent': 'curl/8.0.0'
}

# NOTE
# In September 2024, the DevBlogs site was redesigned: https://devblogs.microsoft.com/blog/introducing-the-new-dev-blogs-a-modern-streamlined-and-engaging-experience
# This script has been updated to work with the redesgin; however, the new site introduced a bug whereby blog pages past a certain number incorrectly return 404 (also, JavaScript errors in the console) even though the page exists.
# I've reported this bug as feedback. So, it should hopefully be fixed. Until then, we can only fetch up to page 712 in my tests.
# Luckily, we still have the downloads from before the redesign. However, the new format has changed and we now have comments support. As a result, stored blog entries before March 15, 2005 remain in the old format.
page_number = 1

# NOTE
# This script only gathers the first bunch of comments on an article (about 15).
# The "Load more comments" button requires JavaScript, so this script cannot gather any more.
# There aren't typically many comments on a single article, though.
# In the future, we could do some Playwright automation to get these.
#
# Also know that while most comments are helpful, some of them contain technically misleading information.

while True:
    listing_response = requests.get(f"{PAGE_LISTING_BASE_URL}{page_number}", headers=HEADERS)
    # Read until 404 status or another non-success status
    if listing_response.status_code != 200:
        print(f"Error status fetching article listing for: {listing_response.status_code}")
        break

    print(f"Page: {page_number}")

    # I've confirmed (by testing with a payload) that HTMLParser is NOT vulnerable to XXE
    # https://bugs.launchpad.net/lxml/+bug/1742885
    # https://lxml.de/4.0/api/lxml.etree.HTMLParser-class.html
    listing_html = listing_response.content
    listing_tree = etree.fromstring(listing_html, etree.HTMLParser())
    entry_links = listing_tree.iterfind("body//main//h3/a")

    for entry_link in entry_links:
        link = entry_link.get("href")
        print(f"Link: {link}")

        entry_html = requests.get(link, headers=HEADERS).content
        entry_tree = etree.fromstring(entry_html, etree.HTMLParser())

        # Get the metadata so we can add it to the searchable output
        # This includes valuable information like the title, author(s), and published and modified dates
        meta_tree = entry_tree.findall("head/meta")
        meta_text = ""
        for meta_tag in meta_tree:
            meta_text += etree.tostring(meta_tag, pretty_print=True).decode()
        # Cleanup output
        meta_output = meta_text.replace('\t', '').replace('\n\n', '\n')

        # The meta tags don't include article:tag metadata, so manually parse those fields out here

        # Get the categories
        categories_tree = entry_tree.findall("body//main//a[@data-bi-area='body_category']")
        categories_text = ""
        for category_tag in categories_tree:
            categories_text = ''.join(category_tag.itertext()) + ", "
        categories_output = f"Categories: {categories_text.rstrip(', ')}\n"

        # Get the topics
        topics_tree = entry_tree.findall("body//main//a[@data-bi-area='body_topics']")
        topics_text = ""
        for topic_tag in topics_tree:
            topics_text += ''.join(topic_tag.itertext()) + ", "
        topics_output = f"Topics: {topics_text.rstrip(', ')}\n"

        # Get the article contents
        article_tree = entry_tree.find("body//main//article")
        article_text = ''.join(article_tree.itertext())
        # Clean up and put extra newline before article contents for spacing
        article_output = "\n" + article_text.lstrip().rstrip()

        # Get the comments
        comments_tree = entry_tree.find("body//main//ul[@class='commentlist']")
        comments_text = ''.join(comments_tree.itertext())
        # Cleanup comments output:
        # 1. Remove tabs
        # 2. Remove extraneous newlines
        #   - Replace groups of three newlines so the content of each
        #     comment stays on its own separate line (for easy grepping)
        # 3. Remove trailing spaces before each newline
        # 4. Leading/trailing whitespace trim
        comments_output = re.sub(r'[ ]+\n', '\n', comments_text.replace('\t', '')
                          .replace('\n\n\n', ' ')).lstrip().rstrip()

        # Use article path substring as its identifier
        article_path_part = ''.join(link.split("/")[-2:])
        # Filter for alphanumeric characters only to prevent a local file inclusion vulnerability
        article_file_name = re.sub(r"[^\da-zA-Z]", "", article_path_part)

        # Store article then grep later because there are lots of articles
        # So, we want to reduce slow network I/O
        with open(f"{OUTPUT_DIRECTORY}/articles/{article_file_name}", 'w') as article_file:
            article_file.write(meta_output)
            article_file.write(categories_output)
            article_file.write(topics_output)
            article_file.write(article_output)

        # Store comments in a separate file
        with open(f"{OUTPUT_DIRECTORY}/comments/{article_file_name}", 'w') as comments_file:
            comments_file.write(comments_output)


    page_number += 1
