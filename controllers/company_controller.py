#!/usr/bin/env python
# encoding: utf-8
"""
company_controller.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-17.
Compyright (c) 2010 __MyCompanyName__. all rights reserved.
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Company
from controllers.base_controller import BaseController
from controllers.base_controller import GetTemplate


class CompanyProfileController(BaseController):
    def get(self, company_name):
        url_name = Company.UrlName(company_name)
        company = Company.all().filter("urlname = ", url_name).fetch(1)
        if company:
            company = company[0]
        else:
            self.CompanyNotFound(company_name)
            return
        template_data = {
            'company': company,
            'reviews': [(r.text, r.rating.WeightedAverage())
                        for r in company.GetReviews(order='-date') if r.rating]
            }
        self.Render(GetTemplate('company_profile'), template_data)

    def CompanyNotFound(self, company_name):
        self.Render(GetTemplate('company_not_found'),
                    {'company': company_name})


class CompanyAddController(BaseController):
    def get(self):
        path = GetTemplate('company_add')
        self.Render(path, {})

    def post(self):
        company = Company()
        company.name = self.GetParam('name')
        company.industry = self.GetParam('industry')
        company.url = self.GetParam('url')
        company.put()
        self.redirect('/companies/view/' + company.urlname)


class CompaniesController(BaseController):
    def get(self):
        path = GetTemplate('company_list')
        companies = Company.all().order('name')
        autocomplete_list = ','.join(['"%s"' % c.name for c in companies])
        template_data = {
            'companies': companies,
            'autocomplete_list': autocomplete_list
            }
        self.Render(path, template_data)

application = webapp.WSGIApplication([
        ('/companies/?', CompaniesController),
        ('/companies/add/?', CompanyAddController),
        ('/companies/view/(.*)', CompanyProfileController)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
