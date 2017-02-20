from webpage import WebPage
from collections import deque
from collections import defaultdict
from urlparse import urlparse
import json
import os
import urllib2
from rules.SameDomainRule import SameDomainRule

class Crawler(object):
  def __init__(self, seed_url):
    # get final url after redirections
    seed_url = urllib2.urlopen(seed_url).geturl()
    self.seed_url = urlparse(seed_url)
    self.url_queue = deque([seed_url])
    self.discovered = defaultdict(lambda: None)
    self.unvisited = defaultdict(lambda: None)
    self.discovered[seed_url] = True
    self.unvisited[seed_url] = True
    self.assets = [] 
    self.same_domain_rule  = SameDomainRule(self.seed_url.netloc)
    self.MAX_LINKS_TO_VISIT = 2000
  
  # BFS
  def crawl(self):

    while len(self.url_queue) > 0 and len(self.discovered) <= self.MAX_LINKS_TO_VISIT:
      url = self.url_queue.popleft()
     
      if 'DEBUG' in os.environ:
        print "Queue Size:", len(self.url_queue)
        print "Fetching: ", url
      
      webpage = WebPage(url) 
      self.unvisited[url] = False

      all_links = webpage.get_anchors(False) # False: dont keep fragments
      all_assets = webpage.get_assets() 
      self.assets.append({ 'url': url, 'assets': all_assets})

      for link in all_links:

        # if belongs to same domain & is not already discovered
        if self.same_domain_rule.matches(link) and self.discovered[link.geturl()] is None:
          self.discovered[link.geturl()] = True
          # process if not already in the queue 
          if self.unvisited[link.geturl()] is None: 
            self.url_queue.append(link.geturl())
            self.unvisited[link.geturl()] = True


  def assets_json(self):
    return json.dumps(self.assets, indent=2)  
             
