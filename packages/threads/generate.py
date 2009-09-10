
from OCC.Geom import *
from OCC.Geom2d import *
from OCC.GCE2d import *
from OCC.BRepLib import *
from OCC.BRepBuilderAPI import *
from OCC.BRepOffsetAPI import *
from OCC.gp import *
import math

from gui import display, start_display

radius = 1
turns = 5
cyl = Geom_CylindricalSurface(gp_Ax3(gp_Pnt(0,0,0), gp_Dir(0,0,1)), radius).GetHandle()
slope = GCE2d_MakeSegment(gp_Pnt2d(0,0), gp_Pnt2d(turns*2*math.pi, 1)).Operator()
helix = BRepBuilderAPI_MakeEdge(slope, cyl).Edge()
helix = BRepBuilderAPI_MakeWire(helix).Wire()

#what a fucking pain in the ass
circle = gp_Circ(gp_Ax2(gp_Pnt(radius,0,0), gp_Dir(0,1,0)), 0.05)
circle_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
circle_wire = BRepBuilderAPI_MakeWire(circle_edge).Wire()
circle_face = BRepBuilderAPI_MakeFace(circle_wire).Shape()

print helix.Closed()
print circle_edge.Closed()
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
sweep = BRepPrimAPI_MakePrism(circle_face, gp_Vec(0,1,0)).Shape()
#sweep = BRepOffsetAPI_MakePipe(helix, circle_edge).Shape()


display.DisplayShape(helix)
display.DisplayShape(circle_face)
display.DisplayShape(sweep)
start_display()
