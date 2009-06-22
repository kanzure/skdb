#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later
#unit unit test test, for skdb.py

import unittest
import skdb

class TestUnits(unittest.TestCase):
    def test_nounits(self):
        self.assertEqual(skdb.Unit(None), skdb.Unit(0))
        self.assertEqual(skdb.Unit(0), skdb.Unit(0))
        self.assertEqual(skdb.Unit('-1'), skdb.Unit('0-1'))
        self.assertEqual(skdb.Unit('1-1'), skdb.Unit(0))
        self.assertTrue(skdb.Unit(0).compatible(skdb.Unit(1)))
        self.assertTrue(skdb.Unit(1234).compatible(skdb.Unit(1)))
        self.assertTrue(skdb.Unit(-1).compatible(skdb.Unit(1)))
        self.assertEqual(str(skdb.Unit('1/0').simplify()), 'inf') #hmmmm
    def test_imaginary(self):
        self.assertTrue(skdb.Unit('nanometer').check()) #actually i dont think we will ever see 'nano' in the result
        self.assertRaises(skdb.NaNError, skdb.Unit,'sqrt(-1)')
        self.assertRaises(skdb.NaNError, skdb.Unit,'sqrt(-1mm^2)')
        self.assertRaises(skdb.NaNError, skdb.Unit,'(-1.5e2mm^3)^(1/3)')
        self.assertRaises(skdb.NaNError, skdb.convert,'sqrt(-1)', '1')

      
    def test_weirdshit(self):
        badunits = ['foobar', 
            '..', '...', '1...1',
            '++', '--', '//', '**', '&', '#', '@', '!', '<', '>', ',', '=', '_',]
            #'1.2.3', #i guess this is all right after all (1.2 * 0.3)
        for i in badunits:
            self.assertRaises(skdb.UnitError, skdb.Unit, i)
    def test_order_of_operations(self):
        self.assertEqual(skdb.Unit('25.4mm').to('inch'), skdb.Unit('in').to('25.4mm'))
        self.assertEqual(skdb.Unit('2mm'), skdb.Unit('sqrt(4mm^2)'))
    def test_check(self):
        self.assertTrue(skdb.check(0))
        self.assertTrue(skdb.check(None)) #do we really want None to pass?
        self.assertTrue(skdb.check('mm'))
        self.assertTrue(skdb.check('in-25.4mm'))
        self.assertTrue(skdb.check('25.4mm'))
        self.assertFalse(skdb.check('inch+second'))
        self.assertRaises(skdb.UnitError, skdb.Unit, 'inch+second')
    def test_compatible(self):
        self.assertTrue(skdb.Unit('25.4mm').compatible(skdb.Unit('in')))
        self.assertFalse(skdb.Unit('inch').compatible(skdb.Unit('second')))
        self.assertTrue(skdb.Unit('inch').compatible('inch'))
        self.assertFalse(skdb.Unit('inch').compatible('blargh'))
    def test_nonscalar(self):
        self.assertEqual(skdb.Unit('tempF(212)'), skdb.Unit('tempC(100)'))

class TestScrew(unittest.TestCase):
    def test_conversions(self):
            screw = skdb.load('screw.yaml')['screw'] #yaml.load(open('screw.yaml'))['screw']
            #print yaml.dump(screw)
            self.assertEqual(screw.thread.clamping_force('20N*m/rev'), '354.02982*lbf')
            self.assertEqual(screw.thread.clamping_force('100ft*lbf'), '15079.645*lbf')
            self.assertEqual(screw.thread.tensile_area(), '0.031820683*in^2')
            self.assertEqual(screw.thread.minor_diameter(), '0.1850481*in')
            self.assertEqual(screw.thread.pitch_diameter(), '0.21752041*in')
            self.assertEqual(screw.max_force(), '2704.758*lbf')
            self.assertEqual(screw.breaking_force(), '3500.275*lbf')
if __name__ == '__main__':
    unittest.main()
