#!/usr/bin/python
'''tests pymates.Part'''
import unittest
import copy
import pymates

class TestPart(unittest.TestCase):
    '''tests pymates.Part'''
    def setUp(self):
        #put some variables here
        screw1 = pymates.Part(name="screw")
        bearing1 = pymates.Part(name="bearing")

        def test_part_compatibility(self):
            #screw1+screw1 #assert exception
            #bearing1+bearing1 #assert exception
            self.assertTrue((screw1+bearing1).parts.contains(screw1))
            self.assertTrue((screw1+bearing1).parts.contains(bearing1))
            self.assertTrue(pymates.compatibility(screw1,bearing1)==1)
            self.assertTrue(pymates.compatibility(bearing1,screw1)==1)
            self.assertFalse(pymates.compatibility(screw1,copy.copy(screw1))==1)
            self.assertFalse(pymates.compatibility(bearing1,copy.copy(bearing1))==1)
            
            pass
        def test_assembly_options(self):
            #figure out how to represent multiple possible assemblies
            #of two (or more) given parts
            pass
        def test_part_equality(self):
            #are two parts given the same information the same?
            pass
        def test_part_methods(self):
            #in the case of the screw, test the package methods?
            pass

if __name__ == '__main__':
    unittest.main()
