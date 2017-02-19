from bs4 import BeautifulSoup as BS
import requests
from urlparse import urlparse

class WebPage(object):

  def __init__(self, url):
    self.page = requests.get(url) 
    self.soup = BS(self.page.text, "html.parser")

  def get_assets(self):
    assets = []
    assets += self.get_javascript()
    assets += self.get_images()
    assets += self.get_links()
    assets += self.get_anchors()
    return assets

  def __resource(self, element, attribute):
    resources = []
    resources += self.soup.find_all(element)
    url_strings = filter(lambda val: val is not None, map(lambda res: res.get(attribute), resources))
    urls = map(lambda url_str: urlparse(url_str), url_strings)
    return urls

  def get_javascript(self):
    return self.__resource('script', 'src')

  def get_images(self):
    return self.__resource('img', 'src')

  def get_links(self):
    return self.__resource('link', 'href')

  def get_anchors(self):
    return self.__resource('a', 'href')
