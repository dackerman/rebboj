#!/usr/bin/env python
# encoding: utf-8
"""
index_controller.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Review
from controllers.base_controller import BaseController
from controllers.base_controller import GetTemplate


class JobberHomeController(BaseController):
    def get(self):
	reviews = db.GqlQuery("SELECT * FROM Review ORDER BY date DESC LIMIT 5")
	template_values = {
		'reviews' : reviews
	}
        self.Render(GetTemplate('index'), template_values)

application = webapp.WSGIApplication([('/', JobberHomeController)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

