# crawler

Just messing around with web crawling

## The actual module crawler.py

### Functions

##### recursively_crawl(url, stop_after=None)

Start recursively crawling from the specified url

### Details

##### Web crawling is done by bugs

*   RecursiveBug
*   ConcurrentBug (not implemented) 

##### Doing stuff with HTML is done by content handlers

*   PageTitleContentHandler (not implemented)

A content handler should provide the method `handle_html: [str] => bool`

##### Links are processed by link processors for filtering, etc (not implemented)

*   BasicLinkProcessor (not implemented)

A link processor should provide the method `process_links: [str] => [str]`

##### Requests for HTML is done by request handlers (not implemented)

*   RequestHandler

A request handler should provide the method `scrape_url_for_links: str => [str]`

##### Tracking visited links is done by link trackers

*   DictionaryLinkTracker

A link tracker should provide the following interface:

*   `visited: str => bool`
*   `visit: str => None`
*   `get_visited: - => [(str, int)]`