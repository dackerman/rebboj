#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import db

class Company(db.Model):

    def GetReviews(self):
        query = Review.all().filter('company = ', self)
        reviews = []
        for entry in query:
            reviews.append(entry)
        return reviews

class Review(db.Model):
    text = db.StringProperty(multiline=True)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    company = db.ReferenceProperty(Company)
