# Microsoft Developer Blogs Search

This repo provides a simple and helpful Python script for downloading [Microsoft Developer Blogs](https://devblogs.microsoft.com) articles. We can then comprehensively search the text of the downloaded articles.

The Microsoft Developer Blogs integreated search tool hardly works to find what you're looking for in my experience (also, the search button is broken on Firefox). Microsoft Developer Blogs has RSS feeds but they only store back to the few most recent articles. The Developer Blogs site uses WordPress (on the [WP Engine platform](https://wpengine.com), according to the HTTP `X-Powered-By` response header), so we cannot pull from a public GitHub repo either. Google can be hit-or-miss (especially for technical terms). Hence, this fully local solution provides the most effective way to search articles by first parsing the website's HTML and grabbing each one individually.

This script was originally made for [learning about the Windows loader](https://github.com/ElliotKillick/operating-system-design-review/tree/main/data/windows/ms-devblogs-search) from the perspective of Microsoft Windows developers (since they may have extensive and insider Windows experience, potentially including writing the code or source code access). To get started quickly with searching Old New Thing articles (typically covering Win32/NT), I have provided the pre-downloaded copies here to save everyone some time (up-to-date as of April 22, 2025).

## License

MIT License - Copyright (C) 2024-2025 Elliot Killick <contact@elliotkillick.com>

Articles in this repo are the sole intellectual property of their author. Redistribution of this public work falls under [fair use](https://copyright.psu.edu/copyright-basics/fair-use/) due to transformative, educational, and non-commercial use. All of the articles contained here are necessary for the transformative purpose of bulk searching to learn from, comment on, and critique the work (similar to how Google search operates). This search tool aims to find and promote the relevant work. Also, archiving the articles is helpful because Microsoft has a history of breaking links to Developer Blogs without sufficient redirects. Please visit the Microsoft Developer Blogs website for the optimal viewing experience when reading Developer Blogs. **Thank you to the authors and contributors of the Developer Blogs for their work!**
