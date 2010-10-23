#!/usr/bin/env python
# encoding: utf-8
"""
company_controller.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-17.
Compyright (c) 2010 __MyCompanyName__. all rights reserved.
"""

import os
import cgi

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Company


class CompanyProfileController(webapp.RequestHandler):
    def get(self, company_name):
        path = os.path.join(os.path.dirname(__file__),
                            '../views/company_profile.html')
        company = Company.all().filter("name = ", company_name).fetch(1)[0]
        template_data = {
            'name': company_name,
            'stars': company.GetRating(),
            'reviews': [(r.text, r.rating.WeightedAverage())
                        for r in company.GetReviews(order='-date') if r.rating]
            }
        self.response.out.write(template.render(path, template_data))


class CompaniesController(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),
                            '../views/company_list.html')
        companies = Company.all().order('name')
        template_data = {
            'companies': companies
            }
        self.response.out.write(template.render(path, template_data))

application = webapp.WSGIApplication([
        ('/companies/', CompaniesController),
        ('/companies/(.*)', CompanyProfileController)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
