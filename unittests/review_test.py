#!/usr/bin/env python
# encoding: utf-8
"""
review_test.py

Created by David Ackerman on 2010-10-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import unittest
from ..models.review import Review

class ReviewTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass
  
  def test_creation(self):
    model = Review(text='test')
    model.put()
    fetched_model = Review.all().filter('text = ','test').fetch(1)[0]
    self.assertEquals(fetched_model.text, 'test')

    
if __name__ == '__main__':
  unittest.main()