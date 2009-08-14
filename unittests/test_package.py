#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import unittest
import skdb
name = 'screw'

class TestPackage(unittest.TestCase):
    def test_package_file(self):
        myfile = skdb.package_file(name, 'metadata.yaml')
        self.assertTrue(isinstance(myfile, file))
    def test_load_metadata(self):
        md = skdb.load(skdb.package_file(name, 'metadata.yaml'))
        self.assertTrue(isinstance(md, skdb.Package))
        self.assertTrue(isinstance(md.template, skdb.Template))
        self.assertTrue(isinstance(md.template.parts[0], skdb.Part))
    def test_open_package(self):
        '''tests skdb.open_package'''
        lego = skdb.load_package(name)
        self.assertTrue(isinstance(lego, skdb.Package))
        self.assertTrue(lego.makes_sense())
    def test_md_then_data(self):
        package = skdb.load_package('screw')
        package.load_data('metadata.yaml')
         
        package.load_data('data.yaml')
        self.assertTrue(type(package.parts[0] == package.Screw))
    def test_generic_package_compatibile(self):
        '''this tests whether or not two packages are even generically compatible.
        what this means is that it does not check whether or not two parts are compatible,
        but instead checks whether or not two given packages are going to have compatible parts.'''
        lego_package = skdb.load_package(name)
        lego_package2 = skdb.load_package(name)
        self.assertTrue(lego_package.compatible(lego_package2))
        self.assertTrue(lego_package2.compatible(lego_package))
    def test_package_part(self):
        '''this makes sure we can load up a part defined by the package.'''
        part = skdb.load_package(name).load_data().parts[0]
        self.assertTrue(isinstance(part, skdb.Part))
    def test_package_load_data(self):
        '''tests Package's ability to instantiate objects from data.yaml in the package'''
        screw_package = skdb.load_package(name)
        package = screw_package.load_data()
        for part in package.parts: 
            self.assertTrue(part.makes_sense())
         
if __name__ == '__main__':
    unittest.main()
