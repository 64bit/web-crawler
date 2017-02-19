from webpage import WebPage
from collections import deque
from collections import defaultdict
from urlparse import urlparse
import json
import os

class Crawler(object):
  def __init__(self, seed_url):
    self.seed_url = urlparse(seed_url)
    self.url_queue = deque([seed_url])
    self.visited = defaultdict(lambda: None)
    self.visited[seed_url] = True
    self.assets = defaultdict(lambda: None)
  
  # BFS
  def crawl(self):

    while len(self.url_queue) > 0:
      url = self.url_queue.popleft()
      
      if os.environ['DEBUG']:
        print "Fetching: ", url
      
      webpage = WebPage(url) 
      all_links = webpage.get_anchors()
      all_assets = webpage.get_assets()
      self.assets[url] = all_assets

      for link in all_links:

        if os.environ['DEBUG']:
          print "Exploring link: ", link.geturl()       

        if self.visited[link.geturl()] is None:
          self.visited[link.geturl()] = True
          self.url_queue.append(link.geturl())


  def assets_json(self):
    return json.dumps(self.assets)  
             
