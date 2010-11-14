#!/usr/bin/env python
# encoding: utf-8
"""
review_controller.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-23.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Review
from models import Company
from models import Rating
from controllers.base_controller import BaseController
from controllers.base_controller import GetTemplate


class AddReviewController(BaseController):
    def get(self, url_name):
        company = Company.all().filter('urlname = ', url_name).fetch(1)
        company = company[0]
	reviews = db.GqlQuery("SELECT * FROM Review ORDER BY date DESC")
	template_values = {
		'reviews': reviews,
                'company_name': company.name
	}
        self.Render(GetTemplate('review'), template_values)

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


class ListReviewsController(BaseController):
    def get(self, url_name):
        company = Company.all().filter('urlname = ', url_name).fetch(1)
        company = company[0]
        reviews = company.GetReviews();
	template_values = {
		'reviews': reviews,
                'company_name': company.name
	}
        self.Render(GetTemplate('company_reviews'), template_values)


application = webapp.WSGIApplication(
    [('/companies/view/(.*)/reviews/add', AddReviewController),
     ('/companies/view/(.*)/reviews/?', ListReviewsController)],
    debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
