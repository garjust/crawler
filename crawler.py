from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import requests
import sys


def recursively_crawl(url, stop_after=None):
    """
    Recursively crawl starting at url

    If stop_after is specified the crawler stops after visiting 'stop_after' links
    """
    link_tracker = DictionaryLinkTracker()
    request_handler = RequestHandler()
    crawler = RecursiveBug(link_tracker, request_handler)
    if stop_after:
        crawler.exit_function = lambda: len(link_tracker.visited_links) > stop_after 
    crawler.crawl('http://news.google.com')
    return link_tracker


class DictionaryLinkTracker(object):
    """
    Basic dictionary implementation of the link tracker
    """

    def __init__(self):
        self.visited_links = {}

    def visited(self, url):
        if url in self.visited_links:
            self.visited_links[url] += 1
            return True
        return False

    def visit(self, url):
        self.visited_links[url] = 1

    def dump(self, handle):
        for link, count in self.visited_links.items():
            handle.write("%s\t%s\n" % (count, link))


class RequestHandler(object):
    """
    Request handler implemented with requests.get
    """

    def __init__(self):
        self.failed_requests = []

    def scrape_url_for_links(self, url):
        try:
            html = self._scrape_url(url)
        except requests.exceptions.ConnectionError:
            return []
        return self._get_links_from_html(html)

    def _scrape_url(self, url):
        try:
            response = requests.get(url)
        except Exception as exception:
            self.failed_requests.append((url, exception))
            raise exception
        return response.content

    def _get_links_from_html(self, html):
        anchors = BeautifulSoup(html, parseOnlyThese=SoupStrainer('a'))
        return [anchor['href'] for anchor in anchors if anchor.has_key('href')]


class BaseBug(object):

    def __init__(self, link_tracker, request_handler):
        super(BaseBug, self).__init__()
        self.link_tracker = link_tracker
        self.request_handler = request_handler

    def _filter_links(self, links):
        links = filter(self._valid_link, links)
        links = map(self._normalize_link, links)
        links = filter(lambda link: not self.link_tracker.visited(link), links)
        return links

    def _valid_link(self, link):
        if re.match(r'http://.*', link):
            return True
        return False

    def _normalize_link(self, link):
        return re.match(r'(http://[^#]*)', link).group(0)


class RecursiveBug(BaseBug):

    def __init__(self, link_tracker, request_handler, exit_function=None):
        super(RecursiveBug, self).__init__(link_tracker, request_handler)
        self.exit_function = exit_function

    def crawl(self, *urls):
        links = []
        for url in urls:
            self.link_tracker.visit(url)
            raw_links = self.request_handler.scrape_url_for_links(url)
            links += self._filter_links(raw_links)
            if self.exit_function and self.exit_function():
                return
        return self.crawl(*links)


class ConcurrentBug(BaseBug):

    def __init__(self, link_tracker, request_handler, link_queue):
        super(RecursiveBug, self).__init__(link_tracker, request_handler)
        self.link_queue = link_queue

    def start_crawling(self):
        pass

    def stop_crawling(self):
        pass

    def crawl_url(self, url):
        self.link_tracker.visit(url)
        raw_links = self.request_handler.scrape_url_for_links(url)
        return self._filter_links(raw_links)

if __name__ == '__main__':
    recursively_crawl('http://news.google.com', stop_after=20).dump(sys.__stdout__)
