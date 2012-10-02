import httplib2
import re

from BeautifulSoup import BeautifulSoup, SoupStrainer

start_url = ["http://news.google.com"]

visited_links = {}

def visited(url):
  if url not in visited_links:
    visited_links[url] = 0
    return False
  return True

def get_links_from_url(url):
  http = httplib2.Http()
  status, response = http.request(url)

  links = []

  for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
      if re.match(r'http://.*', link['href']):
        # print link['href']
            if not visited(link['href']):
              print link['href']
              links.append(link['href'])

  return links

def crawl(urls):
  links = []
  for url in urls:
    links += get_links_from_url(url)
  crawl(links)

crawl(start_url)