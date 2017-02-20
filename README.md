
#### Intro

Crawls the web within same domain, for example if start url is https://www.google.com, then it won't crawl https://maps.google.com. Crawler limits webpages visited to 2000. Crawler runs a BFS from start url. 

####Usage

The command below prints the static assets (js, css, image, txt, pdf, doc, docx files) url.
```
./crawl https://www.google.com
```

Output of above command: 
```
[ 
  {
    "url": "http://www.google.com/history/optout?hl=en",
    "assets": [
      "https://www.gstatic.com/images/branding/googlelogo/2x/googlelogo_light_color_74x24dp.png",
      "http://www.gstatic.com/history/static/myactivity_20170215-0135_1/angular-material.css",
      "https://fonts.googleapis.com/css?family=RobotoDraft:400,500"
    ]
  },
  ...
  ...
  {
    "url": "http://www.google.com/preferences?hl=en",
    "assets": [
      "https://www.google.com/images/branding/searchlogo/1x/googlelogo_desk_heirloom_color_150x55dp.gif",
      "https://www.google.com/images/warning.gif"
    ]
  }
]
```



To run in verbose mode, so as to see what crawler is doing at current moment:
```
DEBUG=true ./crawl https://www.google.com
```
Snippet of intermediate output of above command, where "Queue Size" is the BFS queue size at given moment, also relative urls are getting converted to absolute url: 

```
...
Queue Size: 334
Fetching:  https://www.google.com/intl/en/about/products/products/
converted:  //www.google.com/  -->  https://www.google.com/
converted:  //www.google.com/  -->  https://www.google.com/
Queue Size: 333
Fetching:  https://www.google.com/intl/en/about/products/products/assistant/
converted:  //www.google.com/  -->  https://www.google.com/
converted:  //www.google.com/  -->  https://www.google.com/
Queue Size: 332
Fetching:  https://www.google.com/intl/en/about/products/products/pixel/
converted:  //www.google.com/  -->  https://www.google.com/
converted:  //www.google.com/  -->  https://www.google.com/
Queue Size: 331
Fetching:  https://www.google.com/intl/en/about/products/products/allo-duo/
converted:  //www.google.com/  -->  https://www.google.com/
converted:  //www.google.com/  -->  https://www.google.com/
Queue Size: 330
...
```

#### Running Unittests
Unittests runs an actual webserver (flask) instead of mocking `requests.get(url)`
```
./run_tests.sh
```

####Dependencies
Python 2.7, requests, beautifulsoup, flask( required by unittests )

####Install Dependencies
```
pip install requests
pip install beautifulsoup4
pip install flask
```
Install other required modules using `pip`
