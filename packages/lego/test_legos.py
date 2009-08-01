#!/usr/bin/python
from lego import Lego, Peg, Hole
from skdb import Part 
import unittest

def init_legos(): #why can't i do this in test_lego?
        global bricklist
        print "hi!"
        brick1 = Lego("brick1", num_pegs=4, num_holes=2)
        brick2 = Lego("brick2", num_pegs=2, num_holes=1)
        brick3 = Lego("brick3", num_holes=3)
        brick4 = Lego("brick4", num_pegs=4)
        brick5 = Lego("brick5", num_pegs=0, num_holes=0)
        #print brick1.interfaces[0].__class__.__name__
        bricklist = [brick1, brick2, brick3, brick4, brick5]

init_legos()

class TestLegos(unittest.TestCase):
    def test_equations(self):
        pass

    def test_dimensions(self):
        #TODO: load up a lego with bad dimensions (make sure it complains)
        pass

    def test_generate_cad(self):
        #test whether or not it can generate a basic OpenCASCADE model
        pass
    
    def test_lego(self):
        brick1 = bricklist[0]
        self.assertTrue(len(brick1.interfaces) == 6)
        self.assertTrue(len(brick1.pegs()) == 4)
        self.assertTrue(len(brick1.holes()) == 2)
    def test_options(self):
        expected = "paste good results here"
        results = bricklist[0].interfaces[0].options(bricklist)
        self.assertEqual(results, expected)
        #print results
    def test_options_peg_peg_hole_hole(self):
        '''good ol' O(n^2) checking. if you're going to be a useless test, might as well do a good job at it'''
        for brick in bricklist:
            #self.assertFalse(brick.interfaces[0].__class__ == brick.interfaces[0].connected.__class__)
            for interface in brick.interfaces:
                for opt in interface.options(bricklist):
                    if1, if2 = opt.interface1, opt.interface2
                    self.assertFalse(if1.__class__ == Peg and if1.connected.__class__ == Peg)
                    self.assertFalse(if1.__class__ == Hole and if2.connected.__class__ == Hole)
    def test_all_filled_up(self):
        '''there should be no more options involving brick1's interface0'''
        ##TODO connect all bricks in bricklist here
        self.assertTrue(len(bricklist[0].interfaces[0].options(bricklist)) == 0)

if __name__ == '__main__':
    unittest.main()

