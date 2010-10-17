#!/usr/bin/env python
# encoding: utf-8
"""
jobber.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import os
from google.appengine.ext.webapp import template

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class JobberHomeController(webapp.RequestHandler):
    def get(self):
	reviews = db.GqlQuery("SELECT * FROM Review ORDER BY date DESC")
	template_values = {
		'reviews' : reviews
	}

	path = os.path.join(os.path.dirname(__file__), 'views/index.html')
	self.response.out.write(template.render(path, template_values))

class ReviewController(webapp.RequestHandler):
    def post(self):

	review = Review()
	review.text = self.request.get('content')
	review.put()
	self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', JobberHomeController),
                                      ('/review', ReviewController)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

