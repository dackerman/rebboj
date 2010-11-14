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

def GetTemplate(view_name):
    return os.path.join(os.path.dirname(__file__),'../views/'+view_name+'.html')

class ReviewController(webapp.RequestHandler):
    def get(self, url_name):
        company = Company.all().filter('urlname = ', url_name).fetch(1)
        company = company[0]
	reviews = db.GqlQuery("SELECT * FROM Review ORDER BY date DESC")
	template_values = {
		'reviews': reviews,
                'company_name': company.name
	}

	path = GetTemplate('review')
	self.response.out.write(template.render(path, template_values))

    def post(self, url_name):
        company = Company.all().filter('urlname = ', url_name).fetch(1)
        company = company[0]

	review = Review()
        review.company = company
	review.text = self.request.get('content')
        rating = Rating()
        rating.overall = self.GetIntOrDefault('overall')
        rating.benefits = self.GetIntOrDefault('benefits')
        rating.salary = self.GetIntOrDefault('salary')
        rating.environment = self.GetIntOrDefault('environment')
        rating.peers = self.GetIntOrDefault('peers')
        rating.location = self.GetIntOrDefault('location')
        rating.growth = self.GetIntOrDefault('growth')
        rating.put()
        review.rating = rating
	review.put()
	self.redirect('/companies/view/' + company.urlname)

    def GetIntOrDefault(self, param):
        value = self.request.get(param)
        if value:
            return int(value)
        return Rating.GetDefaultRating()

application = webapp.WSGIApplication( [('/companies/view/(.*)/review',
                                        ReviewController)], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
