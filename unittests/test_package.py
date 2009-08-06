#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later
#unit unit test test, for skdb.py

import unittest
import skdb
from skdb import Package

class TestPackage(unittest.TestCase): 
    def test_open_package(self):
        '''tests skdb.open_package'''
        lego = skdb.load_package("lego")
        self.assertTrue(lego.makes_sense())
        pass
    def test_load(self):
        '''tests skdb.load'''
        lego = skdb.load_package("lego")
        self.assertTrue(lego.makes_sense())
        pass
    def test_generic_package_compatibile(self):
        '''this tests whether or not two packages are even generically compatible.
        what this means is that it does not check whether or not two parts are compatible,
        but instead checks whether or not two given packages are going to have compatible parts.'''
        lego_package = skdb.load_package("lego")
        lego_package2 = skdb.load_package("lego")
        self.assertTrue(lego_package.compatible(lego_package2))
        self.assertTrue(lego_package2.compatible(lego_package))
    def test_package_part(self):
        '''this makes sure we can load up a part defined by the package.'''
        #some constants for this test
        peg_count = 4 #number of pegs the block should have
        hole_count = 1 #number of holes the block should have
        #load the package
        lego_package = skdb.load_package("lego")
        #make a lego part
        #TODO: Package should load up all classes and add them in to the current namespace (Package.Lego, Package.Hole, etc.)
        block = lego_package.Lego()
        #FIXME: ugh
        #give it some pegs and holes (make a particular lego brick)
        block.setup("block name", num_pegs=peg_count, num_holes=hole_count)
        self.assertTrue(len(block.holes()) == hole_count)
        self.assertTrue(len(block.pegs()) == peg_count)
    def test_package_load_data(self):
        '''tests Package's ability to instantiate objects from data.yaml in the package'''
        screw_package = skdb.load_package("screw")
        screws = screw_package.load_data()
        for screw in screws:
            self.assertTrue(screw.makes_sense())
         
if __name__ == '__main__':
    unittest.main()
