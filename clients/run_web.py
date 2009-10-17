#!/usr/bin/python
from web import *
print "starting cherrypy webserver"
cherrypy.quickstart(Root())

