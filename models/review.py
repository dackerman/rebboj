#!/usr/bin/env python
# encoding: utf-8
"""
review.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""
from google.appengine.ext import db
from company import Company

class Review(db.Model):
    text = db.StringProperty(multiline=True)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    company = db.ReferenceProperty(Company)

    @staticmethod
    def GetReviewsByCompany(company):
        query = Review.all().filter('company = ',company)
        reviews = []
        for entry in query:
            reviews.append(entry)
        return reviews
