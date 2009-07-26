#!/usr/bin/python
import screw
import unittest

class TestScrew(unittest.TestCase):
    def test_breaking_force(self):
        pass

    def test_max_force(self):
        pass

    def test_generate_cad(self):
        #test whether or not it can generate a basic OpenCASCADE model
        pass

    def test_conversions(self):
            screw = screw.skdb.load(open('data.yaml'))['screw'] #yaml.load(open('screw.yaml'))['screw']
            #print yaml.dump(screw)
            self.assertEqual(screw.thread.clamping_force('20N*m/rev'), '354.02982*lbf')
            self.assertEqual(screw.thread.clamping_force('100ft*lbf/rev'), '2400.0*lbf')
            self.assertEqual(screw.thread.tensile_area(), '0.031820683*in^2')
            self.assertEqual(screw.thread.minor_diameter(), '0.1850481*in')
            self.assertEqual(screw.thread.pitch_diameter(), '0.21752041*in')
            self.assertEqual(screw.max_force(), '2704.758*lbf')
            self.assertEqual(screw.breaking_force(), '3500.275*lbf')

if __name__ == '__main__':
    unittest.main()


