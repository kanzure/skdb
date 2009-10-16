#!/usr/bin/python
import os
import sys
sys.stdout = sys.stderr
extra_paths = ["/var/www/", #for skdb on adl.serveftp.org
               "/usr/lib/python2.5/site-packages/",
               "/usr/lib/python2.5/site-packages/Buffet-1.0-py2.5.egg/",
               "/usr/lib/python2.5/site-packages/Cheetah-2.0.1-py2.5-linux-i686.egg/",
               "/usr/lib/python2.5/site-packages/TurboCheetah-1.0-py2.5.egg/",
               os.path.realpath(os.path.curdir), #for templates
              ]
def fix_path():
    '''fixes sys.path only when necessary'''
    for path in extra_paths:
        if path not in sys.path: sys.path.append(path)
fix_path()

#cherrpy
import atexit
import threading
import cherrypy
from cherrypy import _cperror
cherrypy.config.update({'environment': 'embedded'})

#templates
from Cheetah.Template import Template
from templates import *

import unittest
import skdb

def add_newlines(output):
    return output.replace("\n", "\n<br />")

def handle_error():
    '''makes '500 internal server error' not suck'''
    cherrypy.response.status = 500
    cherrypy.response.body = add_newlines(_cperror.format_exc())

class UnitApp(object):
    # def __init__(self):
    #     self._tmpl = IndexTemplate()
    def index(self, *extra, **keywords):
        if len(keywords)==2:
            first = skdb.Unit(keywords[keywords.keys()[0]])
            second = skdb.Unit(keywords[keywords.keys()[1]])
            return str(first.to(second))
        else: raise cherrypy.HTTPError(404, "try units/?one=50+m&two=km")
    index.exposed=True

class Root(object):
    _cp_config = {'request.error_response': handle_error}
    units = UnitApp() #simple example: /units/?one=m&two=km
    def __init__(self):
        self._tmpl = IndexTemplate()
    
    @cherrypy.expose
    def index(self, *extra, **keywords):
        return self._tmpl.respond() #how do i send locals() to cheetah?

class SiteTest(unittest.TestCase):
    def test_newliner(self):
        message="""put text here
        on to the next line"""
        result = add_newlines(message)
        self.assertTrue(result.count("<br />") == 1)

application = cherrypy.Application(Root(), script_name=None, config=None)
if __name__ == "__main__":
    unittest.main()
