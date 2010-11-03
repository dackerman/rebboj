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


def GetTemplate(view_name):
    return os.path.join(os.path.dirname(__file__),'../views/'+view_name+'.html')


class CompanyProfileController(webapp.RequestHandler):
    def get(self, company_name):
        path = GetTemplate('company_profile')
        url_name = Company.UrlName(company_name)
        company = Company.all().filter("urlname = ", url_name).fetch(1)
        if company:
            company = company[0]
        else:
            self.CompanyNotFound(company_name)
            return
        template_data = {
            'name': company_name,
            'stars': company.GetRating(),
            'reviews': [(r.text, r.rating.WeightedAverage())
                        for r in company.GetReviews(order='-date') if r.rating]
            }
        self.response.out.write(template.render(path, template_data))

    def CompanyNotFound(self, company_name):
        path = GetTemplate('company_not_found')
        self.response.out.write(template.render(path, {'company': company_name}))


class CompaniesController(webapp.RequestHandler):
    def get(self):
        path = GetTemplate('company_list')
        companies = Company.all().order('name')
        template_data = {
            'companies': companies
            }
        self.response.out.write(template.render(path, template_data))

application = webapp.WSGIApplication([
        ('/companies/?', CompaniesController),
        ('/companies/(.*)', CompanyProfileController)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
