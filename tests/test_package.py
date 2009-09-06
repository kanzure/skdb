#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import unittest
from skdb import *
from copy import copy, deepcopy
name = 'lego'

class TestPackage(unittest.TestCase):
    def test_unit_test(self):
        '''check whether or not the chosen package is good'''
        pack = Package(name, data=False)
        self.assertTrue(len(getattr(pack, 'source data')) > 0) #yum, data!
        self.assertTrue(check_unix_name(name))
    def test_bare(self):
        '''this tests a bare Package object that doesn't exist'''
        pack = Package("f-32")
        self.assertTrue(isinstance(pack, Package))
        self.assertTrue(not hasattr(pack, "source data"))
        self.assertFalse(os.path.exists(pack.path()))
    def test_loaders(self):
        #first let's test with no data
        package = Package(name, data=False)
        self.assertTrue(isinstance(package, Package))
        self.assertTrue(os.path.exists(package.path())) #but sometimes you just want a package object

        package = Package(name, data=True)
        self.assertTrue(isinstance(package, Package))
        self.assertTrue(package.makes_sense())
        #FIXME test package.template here?
        self.assertTrue(isinstance(package.parts[0], package.Lego))
        self.assertTrue(isinstance(package.parts[0], Part))
        for part in package.parts: #probably unnecessary
            self.assertTrue(part.makes_sense())

        #test archaic way
        package = load_package(name)
        self.assertTrue(isinstance(package.parts[0], package.Lego))
        self.assertTrue(isinstance(package.parts[0], Part))
        self.assertTrue(package.makes_sense)
    def test_generic_package_compatibile(self):
        '''this tests whether or not two packages are even generically compatible.
        what this means is that it does not check whether or not two parts are compatible,
        but instead checks whether or not two given packages are going to have compatible parts.'''
        pack1 = Package(name, data=False)
        pack2 = deepcopy(Package)
        
        self.assertTrue(isinstance(pack1.template, Template))
        self.assertTrue(hasattr(Package, "compatible"))
        self.assertTrue(pack1.compatible(pack2))
        self.assertTrue(pack2.compatible(pack1))
         
if __name__ == '__main__':
    unittest.main()
