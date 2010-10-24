#!/usr/bin/env python
# encoding: utf-8
"""
unittests.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import unittest
import datetime
from google.appengine.api import users
from models import *

class ReviewTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_creation(self):
        review = Review(text='test')
        review.put()
        fetched_review = Review.all().filter('text = ', 'test').fetch(1)[0]
        self.assertEquals(fetched_review.text, 'test')

    def test_author(self):
        user = users.User("testuser@test.com")
        review = Review(author = user)
        review.put()
        fetched_review = Review.all().filter('author = ', user).fetch(1)[0]
        self.assertEquals(fetched_review.author, user)

    def test_rating_review(self):
        testRating = Rating()
        testRating.salary = 5
        testRating.put()
        review = Review(rating=testRating)
        review.put()
        fetched_review = Review.all().filter(
            'rating = ', testRating).fetch(1)[0]
        self.assertEquals(testRating.key(), fetched_review.rating.key())


class CompanyTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_reviews(self):
        testCompany = Company()
        testCompany.put()
        review1 = Review(company=testCompany)
        review2 = Review(company=testCompany)
        review1.put()
        review2.put()
        reviews = testCompany.GetReviews()
        self.assertEquals(2, len(reviews))

    def test_get_reviews_by_date(self):
        testCompany = Company()
        testCompany.put()
        review1 = Review(company=testCompany, text='review1',
                         date=datetime.datetime(2010, 1, 1, 1))
        review2 = Review(company=testCompany, text='review2',
                         date=datetime.datetime(2010, 2, 1, 1))
        review1.put()
        review2.put()
        reviews = testCompany.GetReviews(order='-date')
        self.assertEquals(reviews[0].text, review2.text)
        self.assertEquals(reviews[1].text, review1.text)

    def test_overall_rating(self):
        testCompany = Company()
        testCompany.put()
        rating1 = Rating(overall=1, salary=1,location=1,environment=1)
        rating2 = Rating(overall=2, location=3)
        rating1.put()
        rating2.put()
        review1 = Review(company=testCompany, rating=rating1)
        review2 = Review(company=testCompany, rating=rating2)
        review1.put()
        review2.put()
        self.assertEquals(1.5, testCompany.GetRating())

    def test_name_to_url(self):
        self.assertEquals('onetwothree', Company.UrlName('OneTwoThree'))
        self.assertEquals('one-two-three', Company.UrlName('One Two Three'))
        self.assertEquals('google-inc', Company.UrlName('Google Inc.'))
        self.assertEquals('yahoo', Company.UrlName('Yahoo!'))

    def test_url_name_is_set(self):
        testCompany = Company(name = 'Yahoo!')
        testCompany.put()
        self.assertEquals('yahoo', testCompany.urlname)

class RatingTest(unittest.TestCase):
    def test_creation(self):
        rating = Rating()
        rating.overall = 4
        rating.salary = 3
        rating.growth = 2
        rating.benefits = 5
        rating.peers = 2
        rating.environment = 1
        rating.location = 2
        rating.put()
        fetched_rating = Rating.all().filter(
            'benefits = ', rating.benefits).fetch(1)[0]
        self.assertEquals(rating.key(), fetched_rating.key())
        self.assertEquals(rating.peers, fetched_rating.peers)

    def test_overall_rating(self):
        rating = Rating(overall=5)
        rating.put()
        fetched_rating = Rating.all().filter('overall = ', rating.overall)
        fetched_rating = fetched_rating.fetch(1)[0]
        self.assertEquals(rating.key(), fetched_rating.key())

    def test_initial_weighted_average(self):
        rating = Rating()
        self.assertEquals(3, rating.WeightedAverage())

    def test_weighted_average(self):
        rating = Rating(salary=5)
        self.assertEquals(20 / 6, rating.WeightedAverage())

if __name__ == '__main__':
    unittest.main()
