#!/usr/bin/env python
# encoding: utf-8
"""
unittests.py

Created by David Ackerman & Sweta Vajjhala on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import unittest
from google.appengine.api import users
from models import Company
from models import Review

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


if __name__ == '__main__':
    unittest.main()
