# Microsoft Developer Blogs Search

This repo provides a simple and helpful Python script for downloading [Microsoft DevBlogs](https://devblogs.microsoft.com/) articles. In my tests, the script can download 10 articles every 2.5 seconds, which is fast enough (this is without asynchronous requests). We can then comprehensively search the text of the downloaded articles.

Microsoft DevBlogs has RSS feeds but they only store back to the few most recent articles. The DevBlogs site uses WordPress (on the [WP Engine platform](https://wpengine.com), according to the HTTP `X-Powered-By` response header), so we can't pull from a public GitHub repo either. Google can be hit-or-miss (especially for technical terms). Hence, this fully local solution provides the most effective and powerful way to search articles by first parsing the website's HTML and grabbing each one individually.

This script was originally made for [learning about the Windows loader](https://github.com/ElliotKillick/windows-vs-linux-loader-architecture/tree/main/windows/ms-devblogs-search) from the perspective of Microsoft developers themselves (since they wrote the code and/or have source code access). To get started quickly with searching Old New Thing articles (typically covering Win32/NT), I've provided the pre-downloaded copies here (up-to-date as of May 1st, 2024).

## License

MIT License - Copyright (C) 2024 Elliot Killick <contact@elliotkillick.com>

Articles in this repo are the sole intellectual property of their author.
