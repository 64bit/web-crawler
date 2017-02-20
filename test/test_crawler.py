import unittest
from flask import Flask
from multiprocessing import Process
from crawler import Crawler
import time

class TestCrawler(unittest.TestCase):

  SERVER = "http://127.0.0.1:5000/"
  NO_LINKS_HTML = "<html> <body>Hello World</body> </html>"
  JS_LINKS_HTML = "<html> <head> <script src='/source.js'></script></head> <body>Hello World <script src='/source2.js'></script></body> </html>"
  STYLESHEET_LINKS_HTML = "<html> <head> <link href='/source.css' rel='stylesheet'/> </head> <body>Hello Word</body> </html>"
  IMAGE_LINKS_HTML = "<html> <body><img src='/funny.gif' /> Hello Word</body> </html>"
  ANCHOR_LINKS_HTML = "<html> <body> Hello Word <a href='//what.html' /> <a href='/fetch.html' /> </body> </html>"
  FILE_LINKS_HTML = "<html> <body> Hello Word <a href='/source.pdf' /> <a href='source.txt' /> </body> </html>"
  
  def start_server(self, html):
    # Tests could mock the requests.get(url) call but lets run a real server for testing
    def run_app(args):
      app = Flask("testWebPage")
      @app.route("/")
      def hello():
        return html 
      app.run()
    
    self.flask_process = Process(target=run_app, args=(1,))
    self.flask_process.start()
    # give app some time to be up, otherwise connection will fail
    time.sleep(0.1)

  def tearDown(self):
    self.flask_process.terminate()

  def test_no_links(self):
    self.start_server(TestCrawler.NO_LINKS_HTML)  
    crawler = Crawler(TestCrawler.SERVER)
    crawler.crawl()
    self.assertMultiLineEqual("[\n  {\n    \"assets\": [], \n    \"url\": \"http://127.0.0.1:5000/\"\n  }\n]", crawler.assets_json())


  def test_js_links(self):
    self.start_server(TestCrawler.JS_LINKS_HTML)
    crawler = Crawler(TestCrawler.SERVER) 
    crawler.crawl()
    expected = \
'''[
  {
    "assets": [
      "http://127.0.0.1:5000/source.js", 
      "http://127.0.0.1:5000/source2.js"
    ], 
    "url": "http://127.0.0.1:5000/"
  }
]'''
    self.assertMultiLineEqual(expected, crawler.assets_json())


  def test_stylesheet_links(self):
    self.start_server(TestCrawler.STYLESHEET_LINKS_HTML)
    crawler = Crawler(TestCrawler.SERVER) 
    crawler.crawl()
    expected = \
'''[
  {
    "assets": [
      "http://127.0.0.1:5000/source.css"
    ], 
    "url": "http://127.0.0.1:5000/"
  }
]'''
    self.assertMultiLineEqual(expected, crawler.assets_json())


  def test_image_links(self):
    self.start_server(TestCrawler.IMAGE_LINKS_HTML)
    crawler = Crawler(TestCrawler.SERVER) 
    crawler.crawl()
    expected = \
'''[
  {
    "assets": [
      "http://127.0.0.1:5000/funny.gif"
    ], 
    "url": "http://127.0.0.1:5000/"
  }
]'''
    self.assertMultiLineEqual(expected, crawler.assets_json())


  def test_anchor_links(self):
    self.start_server(TestCrawler.ANCHOR_LINKS_HTML)
    crawler = Crawler(TestCrawler.SERVER) 
    crawler.crawl()
    expected = \
'''[
  {
    "assets": [], 
    "url": "http://127.0.0.1:5000/"
  }, 
  {
    "assets": [], 
    "url": "http://127.0.0.1:5000/fetch.html"
  }
]'''
    self.assertMultiLineEqual(expected, crawler.assets_json())

  def test_file_links(self):
    self.start_server(TestCrawler.FILE_LINKS_HTML)
    crawler = Crawler(TestCrawler.SERVER) 
    crawler.crawl()
    expected = \
'''[
  {
    "assets": [
      "http://127.0.0.1:5000/source.pdf", 
      "http://127.0.0.1:5000/source.txt"
    ], 
    "url": "http://127.0.0.1:5000/"
  }, 
  {
    "assets": [], 
    "url": "http://127.0.0.1:5000/source.pdf"
  }, 
  {
    "assets": [], 
    "url": "http://127.0.0.1:5000/source.txt"
  }
]'''
    self.assertMultiLineEqual(expected, crawler.assets_json())

