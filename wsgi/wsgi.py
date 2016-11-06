#! /usr/bin/env python

import os
import sys
import webapp2

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

WEBPAGE="""\
<!DOCTYPE HTML>
<html>
<head>
  <meta charset="UTF-8">
  <title>Hi there</title>
</head>
<body>

  Looking for something?

  <div style="height: 10px;"> </div>
  
  <button class="trop_btn" onclick="document.location='~adavenpo'">
    Andrew's Page
  </button>

  <div style="height: 10px;"> </div>

  <button class="trop_btn" onclick="document.location='http://www.kathleenandandrew.org'">
    The Wedding Page
  </button>

  <div style="height: 10px;"> </div>
</body>
</html>
"""

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(WEBPAGE)


class QueryPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello')

application = webapp2.WSGIApplication([
    ('/app/', MainPage),
    ('/wsgi/', MainPage),
    ('/wsgi/query', QueryPage), ], debug=True)
