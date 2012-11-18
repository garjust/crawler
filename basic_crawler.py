import re
import requests

from BeautifulSoup import BeautifulSoup, SoupStrainer

start_url = "http://news.google.com"

visited_links = {}
failed_links = []


def visited(url):
    if url not in visited_links:
        visited_links[url] = 0
        return False
    return True


def scrape_url(url):
    try:
        response = requests.get(url)
    except Exception as exception:
        failed_links.append((url, exception))
        raise exception
    return response.content


def is_good_link(link):
    if re.match(r'http://.*', link['href']):
        if not visited(link['href']):
            return link


def get_links_from_html(html):
    links = []
    for link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
        if link.has_key('href'):
            if is_good_link(link):
                print link['href']
                links.append(link['href'])
    return links


def crawl(*urls):
    links = []
    for url in urls:
        try:
            html = scrape_url(url)
        except requests.exceptions.ConnectionError:
            continue
        links += get_links_from_html(html)
    crawl(*links)

if __name__ == '__main__':
    crawl(start_url)