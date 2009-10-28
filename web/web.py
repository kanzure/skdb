#!/usr/bin/python
import os
import sys
sys.stdout = sys.stderr

#compile the templates if necessary
if not os.path.exists("templates/IndexTemplate.py"):
    os.system("cd templates; cheetah compile *.tmpl")

from copy import copy
from string import join

#cherrypy
import atexit
import threading
import cherrypy
from cherrypy.test import helper, webtest
_cperror = cherrypy._cperror
cherrypy.config.update({'environment': 'embedded'})

#cheetah templates
#         __  ____________  __
#         \ \/            \/ /
#          \/    *   *     \/
#           \      |       / 
#            \  ==----==  / 
#             \__________/
#
from Cheetah.Template import Template
from templates import PackageIndex, IndexTemplate, PackageView

import skdb
import unittest

def add_newlines(output):
    return output.replace("\n", "\n<br />")

def handle_error():
    '''makes '500 internal server error' not suck'''
    cherrypy.response.status = 500
    cherrypy.response.body = add_newlines(_cperror.format_exc())

class ManagedPath:
    '''a url is parsed into a ManagedPath. the format is as follows:

    /home/some/page/new/ -->
                             parts = ["home", "some", "page", "new"]
                             cmd = "new"
                             path = ["home", "some", "page"]
    /x/y/z/new/1/2/3     -->
                             parts = ["x", "y", "z", "new", "1", "2", "3"]
                             cmd = "new"
                             path = ["x", "y", "z"]
    
    in "default" methods, this helps send the user somewhere.
    useful for a wiki.
    '''
    reserved_roots = ["account", "admin"] #for /account stuff.
    reserved_words = ["new", "delete", "edit", "history", "source", "archive"]
    def __init__(self, url=str()):
        self._parts = []
        self._cmd = ""
        self._path = []
        if isinstance(url, ManagedPath):
            for (k,v) in url.__dict__: setattr(self, k, copy(v))
        elif isinstance(url, str):
            self._url = url
            self.parse(url)
        elif isinstance(url, tuple):
            self._path = url
            self._url = join(url, "/")
            self.parse(self._url)
    def parse(self, url):
        self._url = url
        if url.count("/") == 0: self._parts = []
        else:
            parts = url.split("/")
            if parts[0] in self.reserved_roots:
                self._cmd = parts[0]
            else:
                path = []
                for part in parts:
                    if part in self.reserved_words:
                        self._cmd = part
                        self._path = path
                        break
                    elif part is not "": path.append(part)
            self._parts = parts
    def __str__(self): return self._url
    def __repr__(self): return str(self)
    def __eq__(self, other):
        '''checks if the path is the same (not the parts)
        so /xyz/new/ matches /xyz/new/123'''
        if other._path == self._path: return True
        else: return False
    def get_path(self):
        if self._path is not []: return self._path
        self.parse(self._url)
        return self._path
    def get_cmd(self):
        if self._cmd is not "": return self._cmd
        self.parse(self._url)
        return self._cmd
    cmd=property(fget=get_cmd, doc="returns which command this url corresponds to")
    path=property(fget=get_path, doc="figures out the path on which the command should operate")

class UnitApp:
    # def __init__(self):
    #     self._tmpl = IndexTemplate()
    def index(self, *extra, **keywords):
        if len(keywords)==2:
            first = skdb.Unit(keywords[keywords.keys()[0]])
            second = skdb.Unit(keywords[keywords.keys()[1]])
            return str(first.to(second))
        else: raise cherrypy.HTTPError(404, "try units/?one=50+m&two=km")
    index.exposed=True

class Uploader:
    '''simple file upload demo- doesn't really do much right now.'''
    def index(self):
        return """
        <html><body>
            <form action="upload" method="post" enctype="multipart/form-data">
            file: <input type="file" name="incoming_file" /><br />
            <input type="submit" />
            </form>
        </body></html>
        """
    index.exposed=True

    def upload(self, incoming_file):
        #get the goods
        handler = incoming_file.file
        contents = handler.read()
        
        #save the file
        #TODO: check if file already exists
        filename = incoming_file.filename
        target = open("templates/" + filename, "w")
        target.write(contents)
        target.close()

        #tell the user
        return "ok thanks, file has been uploaded"
    upload.exposed=True

class Package(PackageView):
    def __init__(self, package):
        PackageView.__init__(self)
        self.package = package
    @cherrypy.expose
    def index(self, **keywords):
        return ("individual package view for Package(" + str(self.package.name) + ")")
    #def __getattr__(self, name):
    #    #find an attribute of this package
    #    #could be a file object, attribute, or method of the package
    #    pass

class PackageSet(skdb.PackageSet, PackageIndex):
    def __init__(self):
        skdb.PackageSet.__init__(self)
        PackageIndex.__init__(self)
    @cherrypy.expose
    def index(self):
        return "PackageSet.index"
    @cherrypy.expose
    def default(self, *vpath, **keywords):
        #default view for a package
        return "PackageSet.default"
    def __getattr__(self, name):
        '''so you can GET /package/screw/'''
        try: return_value = skdb.PackageSet.__getattr__(self, name)
        except ValueError: return cherrypy.Http404()
        return Package(return_value)

class Root(IndexTemplate):
    _cp_config = {'request.error_response': handle_error}

    units = UnitApp() #simple example: /units/?one=m&two=km
    uploader = Uploader()
    package = PackageSet()

    def __init__(self):
        IndexTemplate.__init__(self)
    @cherrypy.expose
    def index(self, *extra, **keywords):
        return self.respond()
    @cherrypy.expose
    def default(self, *virtual_path, **keywords):
        if not virtual_path:
            return self.index(**keywords)
        url = ManagedPath(virtual_path)
        return_value = """
        Root.default(virtual_path=%s, keywords=%s)
        cmd is: %s
        virtual path is: %s
        """ % (str(virtual_path), str(keywords), url.cmd, url.path)
        return add_newlines(return_value)

application = cherrypy.Application(Root(), script_name=None, config=None)

class SiteTest(helper.CPWebCase):
    def test_newliner(self):
        message="""put text here
        on to the next line"""
        result = add_newlines(message)
        self.assertTrue(result.count("<br />") == 1)
    def test_url(self):
        url1 = ManagedPath("/home/index/edit")
        self.assertTrue(url1.cmd == "edit")
        url2 = ManagedPath("/home/index/edit/")
        self.assertTrue(url2.cmd == "edit")
        
        url3 = ManagedPath("/home/index/edit/stuff/goes/here")
        self.assertTrue(url3.cmd == "edit")
        url4 = ManagedPath("/home/index/edit/stuff/goes/")
        self.assertTrue(url4.cmd == "edit")

        url5 = ManagedPath("/home/index/stuff/edit")
        self.assertTrue(url5.path == ["home", "index", "stuff"])
        url6 = ManagedPath("/path/to/the/file/new/extra/stuff/123")
        self.assertTrue(url6.path == ["path", "to", "the", "file"])
    def test_url_eq(self):
        url1 = ManagedPath("/home/index/edit/")
        url2 = ManagedPath("/home/index/edit/blah")
        self.assertTrue(url1 == url2)

        url3 = ManagedPath("/home/index/edit")
        self.assertTrue(url3 == url2)
    def test_package(self):
        self.getPage("/package/lego/", method="GET")
        self.assertStatus(200) #see also assertBody

#http://projects.dowski.com/files/cp22collection/cp22collection.py?version=colorized
def setup_server():
    cherrypy.tree.mount(Root(), '/')
    cherrypy.config.update({
            'server.log_to_screen': False,
            'autoreload.on': False,
            'log_debug_info_filter.on': False,
            'environment': 'test_suite',
    })

if __name__ == "__main__":
    webtest.WebCase.interactive = False
    setup_server()
    helper.testmain()
