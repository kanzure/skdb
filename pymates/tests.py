#!/usr/bin/python

import unittest
import pymates

class TestPrimitives(unittest.TestCase):
    def test_primitive_shape(self):
        #test pymates.geom.primitives.PrimitiveShape
        pass

class TestGeom(unittest.TestCase):
    def test_circle(self):
        #test pymates.geom.Circle
        pass
    def test_square(self):
        #test pymates.geom.Square
        pass

class TestPymates(unittest.TestCase):
    def test_part(self):
        #test pymates.Part
        #test models/blockhole.yaml
        pass
    def test_interface(self):
        pass

if __name__ == '__main__':
    unittest.main()
