import os
from bs4 import BeautifulSoup as BS
import requests
from urlparse import urlparse
from urlparse import urljoin
import mimetypes

mimetypes.init()

class WebPage(object):

  def __init__(self, url):
    self.url = urlparse(url)
    self.page = requests.get(url) 
    self.soup = BS(self.page.text, "html.parser")

  def get_assets(self):
    assets = []
    assets += self.get_js()
    assets += self.get_images()
    assets += self.get_stylesheets()
    assets += self.get_files()
    return map(lambda a: a.geturl(), assets) 

  def __get_url(self, element, attribute, keep_fragments=True):
    resources = []
    resources += self.soup.find_all(element)
    url_strings = filter(lambda val: val is not None, map(lambda res: res.get(attribute), resources))
    
    # parse url as well as convert relative url to absolute url
    def parse_url(url_str):
      # TODO handle tel:11234567890, mailto:someone@somewhere.com
      absolute_url = urljoin(self.page.url, url_str) 

      if not keep_fragments:
        # get rid of fragment
        absolute_url = absolute_url.split("#")[0]

      if 'DEBUG' in os.environ and url_str != absolute_url:
        print "converted: ", url_str, " --> ", absolute_url
      return urlparse(absolute_url) 

    urls = map(parse_url, url_strings)
    return urls

  def get_js(self):
    return self.__get_url('script', 'src')

  def get_images(self):
    return self.__get_url('img', 'src')

  def get_links(self):
    return self.__get_url('link', 'href')

  def get_anchors(self, keep_fragments=True):
    return self.__get_url('a', 'href', keep_fragments)

  def get_stylesheets(self):
    stylesheets = []
    stylesheets += self.soup.find_all('link')
    def sytlesheet_filter(link):
      rel = link.get('rel')[0]      
      if rel == "stylesheet" or rel == "" or rel is None:
        return True
      return False    

    stylesheets = filter(sytlesheet_filter, stylesheets)
    url_strings = map(lambda ss: ss.get('href'), stylesheets)
    urls = map(lambda ss: urlparse(urljoin(self.page.url, ss)), url_strings)
    return urls

  def get_files(self):
    all_anchors = self.get_anchors()
    
    def filter_files(f):
      if "." + f.geturl().split(".")[-1] in mimetypes.types_map.keys(): 
        return True
      return False
  
    return filter(filter_files, all_anchors)


  
