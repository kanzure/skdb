#generate.py: produce standard thread forms using OpenCASCADE
#copyright 2009 Ben Lipkowitz
#you may redistribute this file under the terms of the GNU GPL version 2 or later

from __future__ import division
#for projecting onto a cylinder
from OCC.Geom import *
from OCC.Geom2d import *

from OCC.GeomFill import *
from OCC.GCE2d import * #do i really need to use GCE2d to make a 2d segment?
from OCC.BRep import * #BRep_Tool
#from OCC.BRepLib import *
from OCC.BRepBuilderAPI import *
from OCC.BRepOffsetAPI import *

#for finding the end points
from OCC.TopExp import *
from OCC.TopAbs import *

from OCC.TopoDS import *
from OCC.gp import *
import math

from gui import display, start_display, make_vertex

class Helix:
    def __init__(self, radius, turns, height, axial_offset=0, origin=gp_Ax3(gp_Pnt(0,0,0), gp_Dir(0,0,1))):
        self.radius, self.turns, self.height, self.axial_offset, self.origin = radius, turns, height, axial_offset, origin
        self.cyl = Geom_CylindricalSurface(origin, radius).GetHandle()
        #help(BRepBuilderAPI_MakeEdge)
        self.start2d, self.end2d = gp_Pnt2d(0,0+axial_offset), gp_Pnt2d(turns*2*math.pi, height+axial_offset)
        self.slope = GCE2d_MakeSegment(self.start2d, self.end2d).Operator()

    def _MakeEdge(self, slope, cyl): return BRepBuilderAPI_MakeEdge(slope, cyl) #needed for end_points

    def Edge(self): return self._MakeEdge(self.slope, self.cyl).Edge()

    def end_vertices(self):
        '''the ends of the helix as a list of TopoDS_Vertex's'''
        m = self._MakeEdge(self.slope, self.cyl)
        return [m.Vertex1(), m.Vertex2()]

    def end_points(self):
        '''the ends of the helix as a list of gp_Pnt's'''
        v1, v2 = self.end_vertices()
        return [BRep_Tool().Pnt(v1), BRep_Tool().Pnt(v2)]

    def Curve(self): return BRep_Tool().Curve(self.Edge())[0].GetObject() #segfaults when you try to do anything..

    def Wire(self): return BRepBuilderAPI_MakeWire(self.Edge()).Wire()

major_diameter = 1/2
height = 1
turns = 5
pitch = height/turns
minor_diameter = major_diameter - (pitch * 5/8)
crest1 = Helix(major_diameter/2, turns, height)
crest2 = Helix(major_diameter/2, turns, height, axial_offset=pitch/8)
valley1 = Helix(minor_diameter/2, turns, height, axial_offset=pitch*3/8)
valley2 = Helix(minor_diameter/2, turns, height, axial_offset=pitch*5/8)
root = Helix(minor_diameter/2, turns, height, axial_offset = pitch*9/16)
root_curve = Helix(minor_diameter/2, turns, height, axial_offset = pitch*9/16).Curve()
#    mkFillet.Add(myThickness/12, root)

#this segfaults, why?
#root_points = root_curve.Value(0), root_curve.Value(turns*2*math.pi) 

points = crest1.end_points()
start1, end1= crest1.end_vertices()
start2, end2 = crest2.end_vertices()

startedge = BRepBuilderAPI_MakeEdge(start2, start1).Edge()
display.DisplayShape(startedge)
display.DisplayShape([start1, start2])

endedge = BRepBuilderAPI_MakeEdge(end1, end2).Edge()
display.DisplayShape(endedge)
display.DisplayShape([end1, end2])


tmp = BRepBuilderAPI_MakeWire()
print TopoDS().Edge(endedge.Reversed())
[tmp.Add(edge) for edge in [crest1.Edge(), endedge, TopoDS().Edge(crest2.Edge().Reversed()), startedge ]]
assert tmp.Wire().Closed()
land = BRepBuilderAPI_MakeFace(tmp.Wire())
#print land.Check()
print dir(land)
#display.DisplayShape(land.Shape())

display.DisplayShape(crest1.Edge())
display.DisplayShape(crest2.Edge())
#display.DisplayShape(root)
display.DisplayShape(valley1.Edge())
display.DisplayShape(valley2.Edge())

start_display()
