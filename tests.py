#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later
#unit unit test test, for skdb.py

import unittest
import skdb

class TestUnits(unittest.TestCase):
    def test_imaginary(self):
        self.assertRaises(skdb.NaNError, skdb.Measurement('sqrt(-1)').check)
        self.assertRaises(skdb.NaNError, skdb.Measurement('sqrt(-1mm^2)').check)
        self.assertRaises(skdb.NaNError, skdb.Measurement('(-1.5e2mm^3)^(1/3)').check)
      
    def test_weirdshit(self):
        badunits = ['foobar', 
            '..', '...', '1...1',
            '++', '--', '//', '**', '&', '#', '@', '!', '<', '>', ',', '=', '_',]
            #'1.2.3', #i guess this is all right after all (1.2 * 0.3)
        for i in badunits:
            self.assertRaises(skdb.UnitError, skdb.Measurement(i).check)
    def test_order_of_operations(self):
        self.assertEqual(skdb.Measurement('25.4mm').to('inch'), skdb.Measurement('in').to('25.4mm'))
        self.assertEqual(skdb.Measurement('2mm'), skdb.Measurement('sqrt(4mm^2)'))
    def test_check(self):
        self.assertTrue(skdb.Measurement('mm').check())
        self.assertTrue(skdb.Measurement('in-25.4mm').check())
        self.assertTrue(skdb.Measurement('25.4mm').check())
    def test_compatible(self):
        self.assertTrue(skdb.Measurement('25.4mm').compatible(skdb.Measurement('in')))
    def test_nonscalar(self):
        self.assertEqual(skdb.Measurement('tempF(212)'), skdb.Measurement('tempC(100)'))

if __name__ == '__main__':
    unittest.main()
