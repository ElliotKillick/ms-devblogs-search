#!/usr/bin/python3

# Copyright (C) 2024-2025 Elliot Killick <contact@elliotkillick.com>
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
BLOG_URL = "https://devblogs.microsoft.com/oldnewthing"
OUTPUT_DIRECTORY = PROGRAM_DIRECTORY / "out"

os.mkdir(OUTPUT_DIRECTORY)
os.mkdir(f"{OUTPUT_DIRECTORY}/articles")
os.mkdir(f"{OUTPUT_DIRECTORY}/comments")

# Server may block Python Requests user-agent so report as curl instead
HEADERS = {
    'User-Agent': 'curl/8.0.0'
}

# NOTE
# This script only gathers the first bunch of comments on an article (about 15).
# The "Load more comments" button requires JavaScript, so this script cannot gather any more.
# There aren't typically many comments on a single article, though.
# In the future, we could do some Playwright automation to get these.
#
# Also know that while most comments are helpful, some of them contain technically misleading information.

def special_characters_to_plaintext(data: str) -> str:
    """
    Translate special characters to its plaintext equivalent.

    These Unicode codepoints can be problematic when searching the output.
    """

    # \uHHHH is the escape sequence that represents a U+HHHH Unicode codepoint (in many programming languages including Python)
    # Both the website and Python 3 strings use UTF-8 encoding
    # The given Unicode codepoint is, of course, automatically translated to this encoding
    return (data
           .replace('\u00AD', '')   # Soft hyphen (&shy;): The blogging system may place these in a <code> tag
           .replace('\u200B', '')   # Zero-width space
           .replace('\u200C', '')   # Zero-width non-joiner
           .replace('\u200D', '')   # Zero-width joiner
           .replace('\uFEFF', '')   # Zero-width no-break space
           .replace('\u00A0', ' ')) # Non-breaking space (&nbsp;)

# The blogging software has trouble with high page numbers (over 700 in my tests)
# So, index into the archives sorted from newest to oldest then navigate by page number within each one
blog_response = requests.get(f"{BLOG_URL}", headers=HEADERS)
if blog_response.status_code != 200:
    print(f"Error status fetching blog URL: {listing_response.status_code}")
    print(f"Error status {blog_response.status_code} fetching blog for: {BLOG_URL}")
    exit(1)
blog_html = blog_response.content
# I've confirmed (by testing with a payload) that HTMLParser is NOT vulnerable to XXE
# https://bugs.launchpad.net/lxml/+bug/1742885
# https://lxml.de/4.0/api/lxml.etree.HTMLParser-class.html
blog_tree = etree.fromstring(blog_html, etree.HTMLParser())
blog_archive_links = blog_tree.iterfind("body//main//aside//div[@id='rightContentArchive']//ul/li/a")

for blog_archive_link in blog_archive_links:
    blog_archive_link_url = blog_archive_link.get("href")

    page_number = 1

    while True:
        listing_response = requests.get(f"{blog_archive_link_url}/page/{page_number}", headers=HEADERS)
        # Read pages until 404 status
        if listing_response.status_code == 404:
            break
        if listing_response.status_code != 200:
            print(f"Error status {listing_response.status_code} fetching article listing for: {blog_archive_link_url}")
            exit(1)
        print(f"Listing: {blog_archive_link_url}/page/{page_number}")

        listing_html = listing_response.content
        listing_tree = etree.fromstring(listing_html, etree.HTMLParser())
        entry_links = listing_tree.iterfind("body//main//h3/a")

        for entry_link in entry_links:
            entry_link_url = entry_link.get("href")
            print(f"Article: {entry_link_url}")

            entry_html = requests.get(entry_link_url, headers=HEADERS).content
            entry_tree = etree.fromstring(entry_html, etree.HTMLParser())

            # Get the metadata so we can add it to the searchable output
            # This includes valuable information like the title, author(s), and published and modified dates
            meta_tree = entry_tree.findall("head/meta")
            meta_text = ""
            for meta_tag in meta_tree:
                meta_text += etree.tostring(meta_tag, method='html', encoding='unicode');
            # Cleanup output
            meta_output = meta_text.replace('\t', '').replace('\n\n', '\n')
            meta_output = special_characters_to_plaintext(meta_output)

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
            article_output = special_characters_to_plaintext(article_output)

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
            comments_output = special_characters_to_plaintext(comments_output)

            # Use article path substring as its identifier
            article_path_part = ''.join(entry_link_url.split("/")[-2:])
            # Filter for alphanumeric characters and dash only
            # to prevent a path traversal vulnerability
            article_file_name = re.sub(r"[^\da-zA-Z\-]", "", article_path_part)

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
