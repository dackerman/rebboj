#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

from google.appengine.ext import db


class Company(db.Model):
  name = db.StringProperty()
  def GetReviews(self):
    query = Review.all().filter('company = ', self)
    reviews = []
    for entry in query:
      reviews.append(entry)
    return reviews

  def GetRating(self):
    reviews = self.GetReviews()
    total = 0.0
    for review in reviews:
      if review.rating:
        total += review.rating.WeightedAverage()
    return total / len(reviews)


class Rating(db.Model):
    salary = db.IntegerProperty()
    benefits = db.IntegerProperty()
    growth = db.IntegerProperty()
    peers = db.IntegerProperty()
    environment = db.IntegerProperty()
    location = db.IntegerProperty()

    def WeightedAverage(self):
        default = 3
        num_ratings = 6
        return (self.GetValueOrDefault(self.salary) +
                self.GetValueOrDefault(self.benefits) +
                self.GetValueOrDefault(self.growth) +
                self.GetValueOrDefault(self.peers) +
                self.GetValueOrDefault(self.environment) +
                self.GetValueOrDefault(self.location)) / num_ratings

    def GetValueOrDefault(self, value):
        default = 3
        return value if value else default


class Review(db.Model):
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    company = db.ReferenceProperty(Company)
    text = db.StringProperty(multiline=True)
    rating = db.ReferenceProperty(Rating)


