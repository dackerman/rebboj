#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import re
from google.appengine.ext import db


class Company(db.Model):
  name = db.StringProperty()
  urlname = db.StringProperty()

  @staticmethod
  def UrlName(name):
    return name.lower().replace(' ','-').translate(None, '.,?!')

  def GetReviews(self, order=None):
    query = Review.all().filter('company = ', self)
    if order:
      query = query.order(order)
    reviews = []
    for entry in query:
      reviews.append(entry)
    return reviews

  def GetRating(self):
    reviews = self.GetReviews()
    total = 0.0
    count = 0
    for review in reviews:
      if review.rating:
        total += review.rating.overall or 0
        count += 1
    return total / count

  def SetUrlName(self):
    if self.name:
      self.urlname = Company.UrlName(self.name)

  def put(self):
    self.SetUrlName()
    return super(Company, self).put()


class Rating(db.Model):
    overall = db.IntegerProperty()
    salary = db.IntegerProperty()
    benefits = db.IntegerProperty()
    growth = db.IntegerProperty()
    peers = db.IntegerProperty()
    environment = db.IntegerProperty()
    location = db.IntegerProperty()

    def WeightedAverage(self):
        num_ratings = 6
        return (self.GetValueOrDefault(self.salary) +
                self.GetValueOrDefault(self.benefits) +
                self.GetValueOrDefault(self.growth) +
                self.GetValueOrDefault(self.peers) +
                self.GetValueOrDefault(self.environment) +
                self.GetValueOrDefault(self.location)) / num_ratings

    def GetValueOrDefault(self, value):
        default = Rating.GetDefaultRating()
        return value if value else default

    @staticmethod
    def GetDefaultRating():
      return 3


class Review(db.Model):
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    company = db.ReferenceProperty(Company)
    text = db.StringProperty(multiline=True)
    rating = db.ReferenceProperty(Rating)


