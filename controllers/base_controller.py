#!/usr/bin/env python
# encoding: utf-8
"""
base_controller.py

Created by David Ackerman & Sweta Vajjhala on 2010-11-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import os
import cgi

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class BaseController(webapp.RequestHandler):
    def GetParam(self, name):
        return self.request.get(name)

    def Render(self, template_name, template_data):
        self.response.out.write(template.render(template_name, template_data))

def GetTemplate(view_name):
    return os.path.join(os.path.dirname(__file__),'../views/'+view_name+'.html')
