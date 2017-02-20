import unittest
from flask import Flask
from multiprocessing import Process
from webpage import WebPage
import time

class TestWebPage(unittest.TestCase):

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
    self.start_server(TestWebPage.NO_LINKS_HTML)  
    webpage = WebPage(TestWebPage.SERVER)
    self.assertEqual(0, len(webpage.get_js())) 
    self.assertEqual(0, len(webpage.get_stylesheets()))
    self.assertEqual(0, len(webpage.get_links()))
    self.assertEqual(0, len(webpage.get_anchors()))
    self.assertEqual(0, len(webpage.get_images()))
    self.assertEqual(0, len(webpage.get_files()))

  def test_js_links(self):
    self.start_server(TestWebPage.JS_LINKS_HTML)
    webpage = WebPage(TestWebPage.SERVER) 
    self.assertEqual(2, len(webpage.get_js())) 
    self.assertEqual(0, len(webpage.get_stylesheets()))
    self.assertEqual(0, len(webpage.get_links()))
    self.assertEqual(0, len(webpage.get_anchors()))
    self.assertEqual(0, len(webpage.get_images()))
    self.assertEqual(0, len(webpage.get_files()))

  def test_stylesheet_links(self):
    self.start_server(TestWebPage.STYLESHEET_LINKS_HTML)
    webpage = WebPage(TestWebPage.SERVER) 
    self.assertEqual(0, len(webpage.get_js())) 
    self.assertEqual(1, len(webpage.get_stylesheets()))
    self.assertEqual(1, len(webpage.get_links()))
    self.assertEqual(0, len(webpage.get_anchors()))
    self.assertEqual(0, len(webpage.get_images()))
    self.assertEqual(0, len(webpage.get_files()))

  def test_image_links(self):
    self.start_server(TestWebPage.IMAGE_LINKS_HTML)
    webpage = WebPage(TestWebPage.SERVER) 
    self.assertEqual(0, len(webpage.get_js())) 
    self.assertEqual(0, len(webpage.get_stylesheets()))
    self.assertEqual(0, len(webpage.get_links()))
    self.assertEqual(0, len(webpage.get_anchors()))
    self.assertEqual(1, len(webpage.get_images()))
    self.assertEqual(0, len(webpage.get_files()))

  def test_anchor_links(self):
    self.start_server(TestWebPage.ANCHOR_LINKS_HTML)
    webpage = WebPage(TestWebPage.SERVER) 
    self.assertEqual(0, len(webpage.get_js())) 
    self.assertEqual(0, len(webpage.get_stylesheets()))
    self.assertEqual(0, len(webpage.get_links()))
    self.assertEqual(2, len(webpage.get_anchors()))
    self.assertEqual(0, len(webpage.get_images()))
    self.assertEqual(0, len(webpage.get_files()))
    
  def test_file_links(self):
    self.start_server(TestWebPage.FILE_LINKS_HTML)
    webpage = WebPage(TestWebPage.SERVER) 
    self.assertEqual(0, len(webpage.get_js())) 
    self.assertEqual(0, len(webpage.get_stylesheets()))
    self.assertEqual(0, len(webpage.get_links()))
    self.assertEqual(2, len(webpage.get_anchors()))
    self.assertEqual(0, len(webpage.get_images()))
    self.assertEqual(2, len(webpage.get_files()))
    
