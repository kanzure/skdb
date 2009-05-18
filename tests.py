#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later
#unit unit test test, for skdb.py

import unittest
import skdb

class TestUnits(unittest.TestCase):
    def test_nounits(self):
        self.assertEqual(skdb.Measurement(None), skdb.Measurement(0))
        self.assertEqual(skdb.Measurement(0), skdb.Measurement(0))
        self.assertEqual(skdb.Measurement('-1'), skdb.Measurement('0-1'))
        self.assertEqual(skdb.Measurement('1-1'), skdb.Measurement(0))
        self.assertTrue(skdb.Measurement(0).compatible(skdb.Measurement(1)))
        self.assertTrue(skdb.Measurement(1234).compatible(skdb.Measurement(1)))
        self.assertTrue(skdb.Measurement(-1).compatible(skdb.Measurement(1)))
        self.assertEqual(str(skdb.Measurement('1/0').simplify()), 'inf') #hmmmm
    def test_imaginary(self):
        self.assertTrue(skdb.Measurement('nanometer').check()) #actually i dont think we will ever see 'nano' in the result
        self.assertRaises(skdb.NaNError, skdb.Measurement,'sqrt(-1)')
        self.assertRaises(skdb.NaNError, skdb.Measurement,'sqrt(-1mm^2)')
        self.assertRaises(skdb.NaNError, skdb.Measurement,'(-1.5e2mm^3)^(1/3)')
        self.assertRaises(skdb.NaNError, skdb.convert,'sqrt(-1)', '1')

      
    def test_weirdshit(self):
        badunits = ['foobar', 
            '..', '...', '1...1',
            '++', '--', '//', '**', '&', '#', '@', '!', '<', '>', ',', '=', '_',]
            #'1.2.3', #i guess this is all right after all (1.2 * 0.3)
        for i in badunits:
            self.assertRaises(skdb.UnitError, skdb.Measurement, i)
    def test_order_of_operations(self):
        self.assertEqual(skdb.Measurement('25.4mm').to('inch'), skdb.Measurement('in').to('25.4mm'))
        self.assertEqual(skdb.Measurement('2mm'), skdb.Measurement('sqrt(4mm^2)'))
    def test_check(self):
        self.assertTrue(skdb.check(0))
        self.assertTrue(skdb.check(None)) #do we really want None to pass?
        self.assertTrue(skdb.check('mm'))
        self.assertTrue(skdb.check('in-25.4mm'))
        self.assertTrue(skdb.check('25.4mm'))
        self.assertFalse(skdb.check('inch+second'))
        self.assertRaises(skdb.UnitError, skdb.Measurement, 'inch+second')
    def test_compatible(self):
        self.assertTrue(skdb.Measurement('25.4mm').compatible(skdb.Measurement('in')))
        self.assertFalse(skdb.Measurement('inch').compatible(skdb.Measurement('second')))
        self.assertTrue(skdb.Measurement('inch').compatible('inch'))
        self.assertFalse(skdb.Measurement('inch').compatible('blargh'))
    def test_nonscalar(self):
        self.assertEqual(skdb.Measurement('tempF(212)'), skdb.Measurement('tempC(100)'))

if __name__ == '__main__':
    unittest.main()
