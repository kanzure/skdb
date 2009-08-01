#!/usr/bin/python
from lego import Lego
from skdb import Part 
import unittest

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
        brick1 = Lego("brick1", num_pegs=4, num_holes=2)
        self.assertTrue(len(brick1.interfaces) == 6)
        self.assertTrue(len(brick1.pegs()) == 4)
        self.assertTrue(len(brick1.holes()) == 2)
        brick2 = Lego("brick2", num_pegs=2, num_holes=1)
        brick3 = Lego("brick3", num_holes=3)
        brick4 = Lego("brick4", num_pegs=4)
        brick5 = Lego("brick5", num_pegs=0, num_holes=0)
        #print brick1.interfaces[0].__class__.__name__
        bricklist = [brick1, brick2, brick3, brick4, brick5]

        results = brick1.interfaces[0].options(bricklist)
        #print results
     
        self.assertTrue(pymates.has_no_peg_peg_hole_hole(results))

        #have to convert a set to a list to get to the elements
        list(results)[0].apply()
        #there should be no more options involving brick1's interface0
        self.assertTrue(len(pymates.options(brick1.interfaces[0], bricklist)) == 0)

        results2 = pymates.options(brick1.interfaces[1], bricklist)
        #print results2

        self.assertTrue(pymates.has_no_peg_peg_hole_hole(results2))
        #list(results2)[0].apply()

        pass

    #def test_conversions(self):
    #         screw1 = screw.skdb.load(open('data.yaml'))['screw'] #yaml.load(open('screw.yaml'))['screw']
    #         #print yaml.dump(screw)
    #         self.assertEqual(screw1.thread.clamping_force('20N*m/rev'), '354.02982*lbf')
    #         self.assertEqual(screw1.thread.clamping_force('100ft*lbf/rev'), '2400.0*lbf')
    #         self.assertEqual(screw1.thread.tensile_area(), '0.031820683*in^2')
    #         self.assertEqual(screw1.thread.minor_diameter(), '0.1850481*in')
    #         self.assertEqual(screw1.thread.pitch_diameter(), '0.21752041*in')
    #         self.assertEqual(screw1.max_force(), '2704.758*lbf')
    #         self.assertEqual(screw1.breaking_force(), '3500.275*lbf')

if __name__ == '__main__':
    unittest.main()

