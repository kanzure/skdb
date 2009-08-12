#!/usr/bin/python

import unittest
import pymates
import OCC.gp
import OCC.BRepBuilderAPI
import OCC.BRepPrimAPI
import OCC.BRepAlgoAPI
from skdb import Part, Interface

class TestPymates(unittest.TestCase):
    def test_mating(self):
        #test the mating code
        mate(interface1, interface2)
        self.assertTrue(interface1.position == interface2.position)
    def test_part(self):
        #test models/blockhole.yaml

        #clear the screen
        pymates.restart()
        #reset all parts
        pymates.total_parts = []
        #make a new interface
        block_interface = Interface(name="a hole", point=[0,5,0], orientation=[0,0,1], rotation=90) #i dont know the actual values
        #make the part
        block = Part(description='a rectangular prism',created="2009-07-22",interfaces=[block_interface])
        #make some geometry
        length = 5
        width = 20
        height = 10
        block.shapes = [OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(length, width, height).Shape()]
        #see pythonOCC/samples/Level1/TopologyOperations/topology_operations.py
        cone_height = 4 #height of the cone
        #make a new interface
        peg_interface = Interface(name="a surface", point=[0,0,cone_height], x=-90,z=90)
        #make the peg
        peg = Part(description="a conical peg",created="2009-07-22",interfaces=[peg_interface])
        peg.shapes = [OCC.BRepPrimAPI.BRepPrimAPI_MakeCone(10.,1.,float(cone_height)).Shape()]
        peg_shape = peg.shapes[0]
        trsf = OCC.gp.gp_Trsf()
        #set up some points to make a translation vector
        pt1 = OCC.gp.gp_Pnt(0,0,0)
        pt2 = OCC.gp.gp_Pnt(1,1,5)
        #rotate the peg
        rotation_point = pt1
        rotation_dir = OCC.gp.gp_Dir(0,0,1) #arbitrary choice for test
        rotation_axis = OCC.gp.gp_Ax1(rotation_point, rotation_dir)
        rotation_angle = 90 #degrees (arbitrary choice for test)
        trsf.SetRotation(rotation_axis, rotation_angle)
        #translate (move) the peg
        trsf.SetTranslation(pt1, pt2)
        brep_transform = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(trsf)
        brep_transform.Perform(peg_shape)
        resulting_shape = brep_transform.Shape()
        #test translation
        xyz = trsf._CSFDB_Getgp_Trsfloc()
        x,y,z = xyz.X(), xyz.Y(), xyz.Z()
        xyz2 = pt1.XYZ()
        old_x, old_y, old_z = xyz2.X(), xyz2.Y(), xyz2.Z()
        self.assertFalse( (x,y,z) == (old_x,old_y,old_z) )
        #TODO: test rotation
        
        ##top_loc = OCC.TopLoc.TopLoc_Location(trsf)
        ##peg_shape.Location(top_loc) #trsf.Perform()?

        #now make a cut in the block
        #FIXME: is this a perfect cut? is there some tolerance? is it within six sigma?
        cut = OCC.BRepAlgoAPI.BRepAlgoAPI_Cut(block.shapes[0],peg.shapes[0]).Shape()
        OCC.Display.wxSamplesGui.display.DisplayShape(cut)
        #pause
        #raw_input("pause unit tests and wait for user input")
        return
    def test_interface(self):
        pass
    def test_translation(self):
        pymates.start()
        pymates.restart()
        pymates.demo()
        pymates.mate_parts()
        
        #clear the screen
        pymates.restart()
        #reset all the parts
        pymates.total_parts = []
        #load block/peg part mating demo
        pymates.demo()
        (block, peg) = pymates.total_parts
        block_interface, peg_interface = block.interfaces[0], peg.interfaces[0]
        block_point, peg_point = block_interface.point, peg_interface.point
        occ_point1 = OCC.gp.gp_Pnt(block_point[0], block_point[1], block_point[2])
        occ_point2 = OCC.gp.gp_Pnt(peg_point[0], peg_point[1], peg_point[2])
        pivot_point = OCC.gp.gp_Pnt(0, 0, 0)
        x_rotation = OCC.gp.gp_Dir(1, 0, 0)
        y_rotation = OCC.gp.gp_Dir(0, 1, 0)
        z_rotation = OCC.gp.gp_Dir(0, 0, 1)
        transformation = OCC.gp.gp_Trsf()
        transformation.SetRotation(OCC.gp.gp_Ax1(pivot_point, x_rotation), peg_interface.x)
        #FIXME: do a BRepBuilderAPI_Transform here?
        transformation.SetRotation(OCC.gp.gp_Ax1(pivot_point, y_rotation), peg_interface.y)
        transformation.SetTranslation(occ_point2, occ_point1)
        brep_transform = OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(transformation)
        brep_transform.Perform(peg.shapes[0])
        resulting_shape = brep_transform.Shape()
        top_loc = resulting_shape.Location()
        trsf = top_loc.Transformation()
        xyz = trsf._CSFDB_Getgp_Trsfloc()
        x,y,z = xyz.X(), xyz.Y(), xyz.Z()
        #print "resulting location (x = ", x, ", y = ", y, ", z = ", z, ")"
        #OCC.Display.wxSamplesGui.display.DisplayShape(resulting_shape)
        self.assertTrue(x == block_interface.point[0])
        self.assertTrue(y == block_interface.point[1])
        self.assertTrue(z == block_interface.point[2])
        #TODO: test rotation
        return

if __name__ == '__main__':
    pymates.start()
    unittest.main()
