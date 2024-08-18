# Microsoft Developer Blogs Search

This repo provides a super simple and helpful Python script for downloading [Microsoft DevBlogs](https://devblogs.microsoft.com) articles. We can then comprehensively search the text of the downloaded articles (e.g. with a recursive `grep`).

The Microsoft DevBlogs integreated search tool hardly works to find what you're looking for in my experience (also, the search button is broken on Firefox). Microsoft DevBlogs has RSS feeds but they only store back to the few most recent articles. The DevBlogs site uses WordPress (on the [WP Engine platform](https://wpengine.com), according to the HTTP `X-Powered-By` response header), so we can't pull from a public GitHub repo either. Google can be hit-or-miss (especially for technical terms). Hence, this fully local solution provides the most effective way to search articles by first parsing the website's HTML and grabbing each one individually.

This script was originally made for [learning about the Windows loader](https://github.com/ElliotKillick/windows-vs-linux-loader-architecture/tree/main/windows/ms-devblogs-search) from the perspective of Microsoft developers themselves (since they wrote the code and/or have source code access). To get started quickly with searching Old New Thing articles (typically covering Win32/NT), I've provided the pre-downloaded copies here to save everyone some time (up-to-date as of August 16th, 2024).

## License

MIT License - Copyright (C) 2024 Elliot Killick <contact@elliotkillick.com>

Articles in this repo are the sole intellectual property of their author. Redistribution of this public work falls under [fair use](https://copyright.psu.edu/copyright-basics/fair-use/) due to transformative, educational, and non-commercial use. All of the articles contained here are necessary for the transformative purpose of bulk searching to learn, comment, and critique the work (similar to how Google indexes and publishes caches on websites). This search tool aims to find and promote the relevant work. Also, archiving the articles is helpful because Microsoft has a history of breaking links to Developer Blogs without sufficient redirects. Please visit the Microsoft DevBlogs website for the optimal viewing experience when reading Developer Blogs. **Thank you to the authors and contributors of the Developer Blogs for their work!**
