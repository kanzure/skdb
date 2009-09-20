#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later
#unit unit test test, for skdb.py

import unittest
import skdb
from skdb import Unit

class TestUnits(unittest.TestCase):
    def test_nounits(self):
        self.assertEqual(skdb.Unit(None), skdb.Unit(0))
        self.assertEqual(skdb.Unit(0), skdb.Unit(0))
        self.assertEqual(skdb.Unit('-1'), skdb.Unit('0-1'))
        self.assertEqual(skdb.Unit('1-1'), skdb.Unit(0))
        self.assertTrue(skdb.Unit(0).compatible(skdb.Unit(1)))
        self.assertTrue(skdb.Unit(1234).compatible(skdb.Unit(1)))
        self.assertTrue(skdb.Unit(-1).compatible(skdb.Unit(1)))
    def test_conversion(self):
        self.assertEqual(skdb.Unit('25.4mm').to('in').string, '1.0*in')
        self.assertRaises(skdb.UnitError, skdb.Unit('60 degrees').to, 'rad')
        self.assertRaises(skdb.UnitError, skdb.Unit('60 degrees').to, 'fart')
    def test_inf(self):
        #self.assertEqual(str(skdb.Unit('1/0').simplify()), 'inf') #hmmmm
        pass
    def test_imaginary(self):
        self.assertTrue(skdb.Unit('nanometer').check()) #actually i dont think we will ever see 'nano' in the result
        self.assertRaises(skdb.NaNError, skdb.Unit,'sqrt(-1)')
        self.assertRaises(skdb.NaNError, skdb.Unit,'sqrt(-1mm^2)')
        self.assertRaises(skdb.NaNError, skdb.Unit,'(-1.5e2mm^3)^(1/3)')
        self.assertRaises(skdb.NaNError, skdb.Unit(1).compatible, 'sqrt(-1)')
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
    def test_check(self): #what am i testing here?
        self.assertTrue(skdb.Unit(0).check())
        self.assertTrue(skdb.Unit(None).check()) #do we really want None to pass?
        self.assertTrue(skdb.Unit('mm').check())
        self.assertTrue(skdb.Unit('in-25.4mm').check())
        self.assertTrue(skdb.Unit('25.4mm').check())
        #self.assertFalse(skdb.Unit('inch+second').check())
        self.assertRaises(skdb.UnitError, skdb.Unit, 'inch+second')
    def test_compatible(self):
        self.assertTrue(skdb.Unit('25.4mm').compatible(skdb.Unit('in')))
        self.assertFalse(skdb.Unit('inch').compatible(skdb.Unit('second')))
        self.assertTrue(skdb.Unit('inch').compatible('inch'))
        self.assertFalse(skdb.Unit('inch').compatible('blargh'))
    def test_nonscalar(self):
        self.assertEqual(skdb.Unit('tempF(212)'), skdb.Unit('tempC(100)'))
    def test_add(self):
        self.assertEqual(skdb.Unit('1') + skdb.Unit('1'), skdb.Unit('2'))
        self.assertEqual(skdb.Unit('1m') + skdb.Unit('1yd'), skdb.Unit('1.9144m'))
    def test_mul(self):
        self.assertTrue((skdb.Unit('V') * skdb.Unit('A')).compatible('W'))
        self.assertFalse((skdb.Unit('V') * skdb.Unit('W')).compatible('W'))
        self.assertEqual(skdb.Unit('V') * skdb.Unit('A'), skdb.Unit('A') * skdb.Unit('V'))
    def test_div(self):
        self.assertEqual(1/skdb.Unit('16rev/in'), skdb.Unit('(1/16)*(in/rev)'))
        self.assertEqual(1/skdb.Unit('16rev/in'), 1./skdb.Unit('16rev/in'))
    def test_cmp(self):
        self.assertTrue(skdb.Unit('1') >= skdb.Unit('1'))
        self.assertTrue(skdb.Unit('1') <= skdb.Unit('1'))
        self.assertTrue(skdb.Unit('1m') <= skdb.Unit('1000mm'))
        self.assertTrue(skdb.Unit('1m') <= skdb.Unit('1000mm'))
        self.assertFalse(skdb.Unit('1') < skdb.Unit('1'))
        self.assertFalse(skdb.Unit('1') > skdb.Unit('1'))
        self.assertTrue(skdb.Unit('1m') < skdb.Unit('1001mm'))
    def test_negative_cmp(self): #this may not even make any sense in terms of real measurements, since they should never be negative
        self.assertFalse(skdb.Unit('1') < skdb.Unit('-10'))
        self.assertTrue(skdb.Unit('1') > skdb.Unit('-10'))

        self.assertTrue(skdb.Unit('1') > skdb.Unit('0'))
        self.assertTrue(skdb.Unit('0') > skdb.Unit('-1'))
        self.assertTrue(skdb.Unit('1') > skdb.Unit('-1'))
        self.assertTrue(skdb.Unit('1') < skdb.Unit('0'))
        self.assertTrue(skdb.Unit('0') < skdb.Unit('-1'))
        self.assertTrue(skdb.Unit('1') < skdb.Unit('-1'))
        #now, to the left!
        self.assertFalse(skdb.Unit('0') > skdb.Unit('1'))
        self.assertFalse(skdb.Unit('-1') > skdb.Unit('0'))
        self.assertFalse(skdb.Unit('-1') > skdb.Unit('1'))
        self.assertFalse(skdb.Unit('0') < skdb.Unit('1'))
        self.assertFalse(skdb.Unit('-1') < skdb.Unit('0'))
        self.assertFalse(skdb.Unit('-1') < skdb.Unit('1'))
        
        self.assertTrue(skdb.Unit('0') >= skdb.Unit('0'))
    def test_supplemental_units(self):
        self.assertTrue(skdb.Unit('man').check())
        self.assertTrue(skdb.Unit('5*teeth').compatible('tooth'))
        
    def test_somethingorother(self): #is this even desirable?
        self.assertTrue(skdb.Unit('1') > 0.9)

class TestScrew(unittest.TestCase):
    import skdb.packages.screw.screw as screw
    import skdb.packages.threads.threads as threads
    def test_conversions(self):
            screw_package = skdb.Package("screw")
            screw1 = screw_package.parts[0]
            #screw1 = skdb.load(skdb.package_file('screw', 'data.yaml'))['parts'][0]
            self.assertEqual(screw1.thread.clamping_force('20N*m/rev'), '354.02982*lbf')
            self.assertEqual(screw1.thread.clamping_force('100ft*lbf/rev'), '2400.0*lbf')
            self.assertEqual(screw1.thread.tensile_area(), '0.031820683*in^2')
            self.assertEqual(screw1.thread.minor_diameter(), '0.1850481*in')
            self.assertEqual(screw1.thread.pitch_diameter(), '0.21752041*in')
            self.assertEqual(screw1.max_force(), '2704.758*lbf')
            self.assertEqual(screw1.breaking_force(), '3500.275*lbf')

class TestRange(unittest.TestCase):
    def test_incompatibilities(self):
        self.assertRaises(skdb.UnitError, skdb.Range("1m", "1kg"))
        self.assertRaises(skdb.UnitError, skdb.Range("m", "kg"))
        self.assertRaises(skdb.UnitError, skdb.Range("kg", "m"))
        skdb.Range("1 mg", "g")

#test sympy integration
have_sympy = False
try:
    import sympy.physics.units
    have_sympy = True
except ImportError, err:
    print "sympy.physics.units not tested (ImportError)"

if have_sympy:
    class TestSympyUnits(unittest.TestCase):
        def test_conversion(self):
            m1 = skdb.Unit("m")
            m2 = sympy.physics.units.m
            self.assertTrue(m1.compatible(m2))
            m3 = skdb.Unit(sympy.physics.units.m)
            self.assertTrue(m1.compatible(m3))
            self.assertTrue(m3.compatible(m1))

if __name__ == '__main__':
    unittest.main()
