#!/usr/bin/env python
# encoding: utf-8
"""
review_controller.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-23.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import os
import cgi

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Review
from models import Company
from models import Rating


class ReviewController(webapp.RequestHandler):
    def get(self, company_name):
	reviews = db.GqlQuery("SELECT * FROM Review ORDER BY date DESC")
	template_values = {
		'reviews': reviews,
                'company_name': company_name
	}

	path = os.path.join(os.path.dirname(__file__), '../views/review.html')
	self.response.out.write(template.render(path, template_values))

    def post(self, company_name):
        company = Company.all().filter('name = ', company_name).fetch(1)
        if not len(company):
            company = Company(name=company_name)
            company.put()
        else:
            company = company[0]

	review = Review()
        review.company = company
	review.text = self.request.get('content')
        rating = Rating()
        rating.benefits = int(self.request.get('benefits'))
        rating.salary = int(self.request.get('salary'))
        rating.environment = int(self.request.get('environment'))
        rating.peers = int(self.request.get('peers'))
        rating.location = int(self.request.get('location'))
        rating.growth = int(self.request.get('growth'))
        rating.put()
        review.rating = rating
	review.put()
	self.redirect('/companies/' + company_name)


application = webapp.WSGIApplication( [('/companies/(.*)/review',
                                        ReviewController)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
