#!/usr/bin/python
'''tests pymates.Part'''
import unittest
import copy
import pymates

class TestPart(unittest.TestCase):
    '''tests pymates.Part'''
    def test_part_compatibility(self):
        screw1 = pymates.Part(name="screw")
        bearing1 = pymates.Part(name="bearing")
        lego1 = pymates.Part(name="lego brick")
        lego2 = pymates.Part(name="lego 16x8 breadboard")
        #screw1+screw1 #assert exception
        #bearing1+bearing1 #assert exception
        #.. or should (screw1+screw1) be an assembly with
        #.. no options for how to put the parts together?

        self.assertTrue((screw1+bearing1).parts.contains(screw1))
        self.assertTrue((screw1+bearing1).parts.contains(bearing1))
        self.assertTrue(pymates.compatibility(screw1,bearing1)==1)
        self.assertTrue(pymates.compatibility(bearing1,screw1)==1)
        self.assertFalse(pymates.compatibility(screw1,copy.copy(screw1))==1)
        self.assertFalse(pymates.compatibility(bearing1,copy.copy(bearing1))==1)
        self.assertTrue(pymates.compatibility(lego1,lego2)==1)
        self.assertTrue(pymates.compatibility(lego2,lego1)==1)
        self.assertTrue(pymates.compatibility(lego1,copy.copy(lego1))==1)
        self.assertTrue(pymates.compatibility(lego2,copy.copy(lego2))==1)
         
        pass

    def test_assembly_options(self):
        #figure out how to represent multiple possible assemblies
        #of two (or more) given parts
        pass
    def test_assemblies(self):
        #TODO: test assembly1+assembly1
        #TODO: test assembly1+assembly2
        #TODO: test assembly2+assembly2
        #assembly2-assembly1
        #assembly1-assembly2
        #assembly1*assembly2
        #assembly2*assembly1
        #assembly1 >= assembly2
        #assembly2 >= assembly1
        #assembly1 <= assembly2
        #assembly2 <= assembly1
        #assembly1 == assembly1
        #assembly1 == assembly2
        #assembly2 == assembly2
        #(maybe) assembly2 == assembly1
        #part*assembly #figure out all possible mates?
        #TODO: when should assemblies *not* be able to be combined?
        pass
    def test_part_equality(self):
        #are two parts given the same information the same?
        pass
    def test_part_methods(self):
        #in the case of the screw, test the package methods?
        pass
    def test_legos(self):
        import skdb.packages.legos
        hole_count = 1
        peg_count = 4
        lego1 = skdb.packages.legos.Lego("brick",num_pegs=peg_count,num_holes=hole_count)
        self.assertTrue(len(lego1.holes()) == hole_count)
        self.assertTrue(len(lego1.pegs()) == peg_count)
        return

if __name__ == '__main__':
    unittest.main()
