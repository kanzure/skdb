from __future__ import division
from OCC.Geom import *
from OCC.Geom2d import *
from OCC.GeomFill import *
from OCC.GCE2d import *
from OCC.BRep import *
from OCC.BRepLib import *
from OCC.BRepBuilderAPI import *
from OCC.BRepOffsetAPI import *
from OCC.gp import *
import math

from gui import display, start_display, make_vertex

class Helix:
    def __init__(self, radius, turns, height, axial_offset=0, origin=gp_Ax3(gp_Pnt(0,0,0), gp_Dir(0,0,1))):
        self.radius, self.turns, self.height, self.axial_offset, self.origin = radius, turns, height, axial_offset, origin
        self.cyl = Geom_CylindricalSurface(origin, radius).GetHandle()
        self.slope = GCE2d_MakeSegment(gp_Pnt2d(0,0+axial_offset), gp_Pnt2d(turns*2*math.pi, height+axial_offset)).Operator()

    def Edge(self): return BRepBuilderAPI_MakeEdge(self.slope, self.cyl).Edge()
    def Curve(self): return BRep_Tool().Curve(self.Edge())[0].GetObject() #segfaults when you try to do anything..
    def Wire(self): return BRepBuilderAPI_MakeWire(self.Edge()).Wire()

major_diameter = 1/2
height = 1
turns = 5
pitch = height/turns
minor_diameter = major_diameter - (pitch * 5/8)
crest1 = Helix(major_diameter/2, turns, height).Wire()
crest2 = Helix(major_diameter/2, turns, height, axial_offset=pitch/8).Wire()
valley1 = Helix(minor_diameter/2, turns, height, axial_offset=pitch*3/8).Wire()
valley2 = Helix(minor_diameter/2, turns, height, axial_offset=pitch*5/8).Wire()
root = Helix(minor_diameter/2, turns, height, axial_offset = pitch*9/16).Wire()
#root_curve = Helix(minor_diameter/2, turns, height, axial_offset = pitch*9/16).Curve()
#root_points = root_curve.Value(0), root_curve.Value(turns*2*math.pi)

display.DisplayShape(crest1)
display.DisplayShape(crest2)
#display.DisplayShape(root)
display.DisplayShape(valley1)
display.DisplayShape(valley2)
#display.DisplayShape(make_vertex(root_points[0]))
#display.DisplayShape(make_vertex(root_points[1]))


radius = 1
helix_wire = Helix(radius, 5, 1).Wire()
helix_edge = Helix(radius, 5, 1).Edge()
#what a fucking pain in the ass
circle = gp_Circ(gp_Ax2(gp_Pnt(radius,0,0), gp_Dir(0,1,0)), 0.05)
circle_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
circle_wire = BRepBuilderAPI_MakeWire(circle_edge).Wire()
circle_face = BRepBuilderAPI_MakeFace(circle_wire).Shape()



line_edge = BRepBuilderAPI_MakeEdge(gp_Pnt(radius,0,0), gp_Pnt(radius,0,1)).Edge()
line_wire = BRepBuilderAPI_MakeWire(line_edge).Wire()
line_edge = BRepBuilderAPI_MakeEdge(gp_Pnt(radius,0,0), gp_Pnt(radius,0,1)).Shape()

print helix_wire.Closed()
print circle_edge.Closed()
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
sweep = BRepPrimAPI_MakePrism(circle_face, gp_Vec(0,1,0)).Shape()
#sweep = BRepOffsetAPI_MakePipe(helix, circle_edge).Shape()
#sweep = BRepOffsetAPI_MakePipe(circle_wire, line_edge).Shape()


helix_curve = BRep_Tool().Curve(helix_edge)[0] #wtf
circle_curve = BRep_Tool().Curve(circle_edge)[0]
#aPipe2 = GeomFill_Pipe(helix,TC1,TC2, mode)
#print type(helix_curve)
#aPipe2 = GeomFill_Pipe(helix_curve, circle_curve)
#aPipe2.Perform(0,0)
#aSurface2= aPipe2.Surface()


#ps = BRepOffsetAPI_MakePipeShell(helix)
#ps.Add(circle_wire)
#print 'hi'
#ps.SetMode(True)
#display.DisplayShape(ps.Generated(circle_wire).Last())
#display.DisplayShape(ps.FirstShape())
#print 'here'
#ps.Build()
#sweep = ps.MakeSolid()

#display.DisplayShape(helix_wire)
#display.DisplayShape(circle_face)
#display.DisplayShape(line_edge)
#display.DisplayShape(sweep)
start_display()
