#!/usr/bin/python
import os
import sys
sys.stdout = sys.stderr
extra_paths = ["/var/www/", #for skdb on adl.serveftp.org
               "/usr/lib/python2.5/site-packages/",
               "/usr/lib/python2.5/site-packages/Buffet-1.0-py2.5.egg/",
               "/usr/lib/python2.5/site-packages/Cheetah-2.0.1-py2.5-linux-i686.egg/",
               "/usr/lib/python2.5/site-packages/TurboCheetah-1.0-py2.5.egg/",
               "/home/bryan/code/wsgi/",
               os.path.realpath(os.path.curdir), #for templates
              ]
def fix_path():
    '''fixes sys.path only when necessary'''
    for path in extra_paths:
        if path not in sys.path: sys.path.append(path)
fix_path()

from copy import copy
from string import join

#cherrypy
import atexit
import threading
import cherrypy
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
from templates import *

import unittest
import skdb

def add_newlines(output):
    return output.replace("\n", "\n<br />")

def handle_error():
    '''makes '500 internal server error' not suck'''
    cherrypy.response.status = 500
    cherrypy.response.body = add_newlines(_cperror.format_exc())

class CherryBase(object):
    def default(self, *virtual_path, **keywords): #TODO
        if not virtual_path:
            return self.index(**keywords)
        url = ManagedPath(virtual_path)
        return_value = """
        CherryBase.default(virtual_path=%s, keywords=%s)
        cmd is: %s
        virtual path is: %s
        """ % (str(virtual_path), str(keywords), url.cmd, url.path)
        return add_newlines(return_value)
    default.exposed=True

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

class UnitApp(CherryBase):
    # def __init__(self):
    #     self._tmpl = IndexTemplate()
    def index(self, *extra, **keywords):
        if len(keywords)==2:
            first = skdb.Unit(keywords[keywords.keys()[0]])
            second = skdb.Unit(keywords[keywords.keys()[1]])
            return str(first.to(second))
        else: raise cherrypy.HTTPError(404, "try units/?one=50+m&two=km")
    index.exposed=True

class Uploader(CherryBase):
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

class PackageSet(CherryBase, PackageIndex, skdb.PackageSet):
    def __init__(self):
        skdb.PackageSet.__init__(self)
        CherryBase.__init__(self)
        PackageIndex.__init__(self)

    def __getattr__(self, name):
        '''so you can GET /package/screw/'''
        return PackageSet.__getattr__(name)

class Root(CherryBase, IndexTemplate):
    _cp_config = {'request.error_response': handle_error}
    packages = [] #for keeping skdb packages loaded in memory

    #further apps
    units = UnitApp() #simple example: /units/?one=m&two=km
    uploader = Uploader()
    package = PackageSet()

    def __init__(self):
        IndexTemplate.__init__(self)
    
    @cherrypy.expose
    def index(self, *extra, **keywords):
        return self.respond()

application = cherrypy.Application(Root(), script_name=None, config=None)
if __name__ == "__main__":
    ##for unittest
    #tests = [SiteTest]
    #for test in tests:
    #    #http://stackoverflow.com/questions/79754/unittest-causing-sys-exit/79833#79833
    #    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(test))

    #http://projects.dowski.com/files/cp22collection/cp22collection.py?version=colorized
    from cherrypy.test import helper, webtest
    webtest.WebCase.interactive = False
    def setup_server():
        cherrypy.tree.mount(Root(), '/')
        cherrypy.config.update({
                'server.log_to_screen': False,
                'autoreload.on': False,
                'log_debug_info_filter.on': False,
                'environment': 'test_suite',
        })

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
        def test_list_items(self):
            self.getPage('/widgets/')
            self.assertBody("All the items")

        def test_creator_page(self):
            self.getPage('/widgets/creator')
            self.assertBody("An item creator form")

        def test_create_item(self):
            self.getPage('/widgets/', method="POST")
            self.assertBody('Created a new item')

        def test_item_methods(self):
            expected = {'GET': 'Viewing item 1',
                        'PUT': 'Updated item 1 with {}',
                        'DELETE': 'Deleted item 1',
                        }
            for meth, response in expected.iteritems():
                self.getPage('/widgets/1', method=meth)
                self.assertBody(response)

        def test_item_editor(self):
            self.getPage('/widgets/22;editor')
            self.assertBody('An editor form for item 22')

        def test_405s(self):
            self.getPage('/widgets/10', method='POST')
            self.assertStatus(405)
            self.getPage('/widgets/', method='DELETE')
            self.assertStatus(405)

        def test_404s(self):
            for path in ['/widgets/view', '/widgets/32;foobar',
                            '/widgets/33/editor', '/widgets/fluffy',
                            '/widgets/some/where/out/there']:
                self.getPage(path)
                self.assertStatus(404)

        def test_non_mapped(self):
            """Non-mapped methods should not be available over the web."""
            self.getPage('/widgets/private')
            self.assertStatus(404)
            self.getPage('/widgets/1;private')
            self.assertStatus(404)

        def test_limited(self):
            self.getPage('/readonly/')
            self.assertBody('The list of limited items.')

            #try an unimplemented method
            self.getPage('/readonly/', method="POST")
            self.assertStatus(405)

            self.getPage('/readonly/33')
            self.assertBody('Viewing item 33')

            #try an unimplemented method
            self.getPage('/readonly/33', method='DELETE')
            self.assertStatus(405)
    setup_server()
    helper.testmain()
