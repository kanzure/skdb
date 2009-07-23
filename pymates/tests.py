#!/usr/bin/python

import unittest
import pymates
import OCC.gp
import OCC.BRepBuilderAPI

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
    def test_rotation(self):
        pymates.restart()
        pymates.demo()
        pymates.mate_parts()
        
        #clear the screen
        pymates.restart()
        #reset all the parts
        pymates.total_parts = []
        #load block/peg part mating demo
        pymates.demo()
        block = pymates.total_parts[0]
        peg = pymates.total_parts[1]
        block_interface = block.interfaces[0]
        peg_interface = peg.interfaces[0]
        block_point = block_interface.point
        peg_point = peg_interface.point
        occ_point1 = OCC.gp.gp_Pnt(block_point[0], block_point[1], block_point[2])
        occ_point2 = OCC.gp.gp_Pnt(peg_point[0], peg_point[1], peg_point[2])
        pivot_point = OCC.gp.gp_Pnt(0, 0, 0)
        x_rotation = OCC.gp.gp_Dir(1, 0, 0)
        y_rotation = OCC.gp.gp_Dir(0, 1, 0)
        z_rotation = OCC.gp.gp_Dir(0, 0, 1)
        transformation = OCC.gp.gp_Trsf()
        transformation.SetRotation(OCC.gp.gp_Ax1(pivot_point, x_rotation), peg_interface.x)
        transformation.SetRotation(OCC.gp.gp_Ax1(pivot_point, z_rotation), peg_interface.z)
        transformation.SetTranslation(occ_point2, occ_point1)
        brep_transform = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(transformation)
        brep_transform.Perform(peg.shapes[0])
        resulting_shape = brep_transform.Shape()
        top_loc = resulting_shape.Location()
        trsf = top_loc.Transformation()
        xyz = trsf._CSFDB_Getgp_Trsfloc()
        x,y,z = xyz.X(), xyz.Y(), xyz.Z()
        print "resulting location (x = ", x, ", y = ", y, ", z = ", z, ")"
        #OCC.Display.wxSamplesGui.display.DisplayShape(resulting_shape)
        return

if __name__ == '__main__':
    pymates.start()
    unittest.main()
