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

    def Edge(self): return BRepBuilderAPI_MakeEdge(self.slope, self.cyl).Edge()
       
    def Curve(self): return BRep_Tool().Curve(self.Edge())[0].GetObject() #segfaults when you try to do anything..

    def Wire(self): return BRepBuilderAPI_MakeWire(self.Edge()).Wire()
    
    def endpoints(self):
        vertices = []
        points = []
        aVertexExplorer = TopExp_Explorer(self.Wire(), TopAbs_VERTEX)
        while aVertexExplorer.More():
            cur = aVertexExplorer.Current()
            vertices.append(cur)
            p = BRep_Tool().Pnt(TopoDS().Vertex(cur))
            points.append(p)
            #vertices.append(TopoDS().Vertex(aVertexExplorer.Current()))
            aVertexExplorer.Next()
        return vertices, points

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

vertices, points = crest1.endpoints()
display.DisplayShape([make_vertex(p) for p in points])
print [p.Coord() for p in points]

#why does this fail but endpoints() works? v is at the same address each time??
for v in vertices:
    print 'here'
    print v
    print TopoDS().Vertex(v)
    #pnt = BRep_Tool().Pnt(TopoDS().Vertex(v))
    #print 'hi'
    #print pnt.Coord()
    #print v.Location()
    #print dir(v.Location())
    #display.DisplayShape(v)

display.DisplayShape(crest1.Edge())
display.DisplayShape(crest2.Edge())
#display.DisplayShape(root)
display.DisplayShape(valley1.Edge())
display.DisplayShape(valley2.Edge())
#display.DisplayShape(make_vertex(root_points[0]))
#display.DisplayShape(make_vertex(root_points[1]))

radius = 1
helix_wire = Helix(radius, 5, 1).Wire()
helix_edge = Helix(radius, 5, 1).Edge()

#display.DisplayShape(helix_wire)
#display.DisplayShape(circle_face)
#display.DisplayShape(line_edge)
#display.DisplayShape(sweep)
start_display()
