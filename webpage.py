import os
from bs4 import BeautifulSoup as BS
import requests
from urlparse import urlparse
from urlparse import urljoin

class WebPage(object):

  def __init__(self, url):
    self.url = urlparse(url)
    self.page = requests.get(url) 
    self.soup = BS(self.page.text, "html.parser")

  def get_assets(self):
    assets = []
    assets += self.get_js()
    assets += self.get_images()
    assets += self.get_links()
    return map(lambda a: a.geturl(), assets) 

  def __resource(self, element, attribute):
    resources = []
    resources += self.soup.find_all(element)
    url_strings = filter(lambda val: val is not None, map(lambda res: res.get(attribute), resources))
    
    # parse url as well as convert relative url to absolute url
    def parse_url(url_str):
      # TODO handle tel:11234567890
      absolute_url = urljoin(self.page.url, url_str) 
      if os.environ['DEBUG'] and url_str != absolute_url:
        print "converted: ", url_str, " --> ", absolute_url
      return urlparse(absolute_url) 

    urls = map(parse_url, url_strings)
    return urls

  def get_js(self):
    return self.__resource('script', 'src')

  def get_images(self):
    return self.__resource('img', 'src')

  def get_links(self):
    return self.__resource('link', 'href')

  def get_anchors(self):
    return self.__resource('a', 'href')
