crawler
=======

Just messing around with web crawling

The actual module crawler.py
----------------------------

### Functions

##### recursively_crawl(url, stop_after=None)

Start recursively crawling from the specified url

### Details

##### Web crawling is done by bugs

*   RecursiveBug
*   ConcurrentBug (not implemented) 

##### Requests for HTML is done by request handlers

*   RequestHandler

##### Tracking visited links is done by link trackers

*   DictionaryLinkTracker