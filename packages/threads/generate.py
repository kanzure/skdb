
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

from gui import display, start_display

radius = 1
turns = 0.5
cyl = Geom_CylindricalSurface(gp_Ax3(gp_Pnt(0,0,0), gp_Dir(0,0,1)), radius).GetHandle()
slope = GCE2d_MakeSegment(gp_Pnt2d(0,0), gp_Pnt2d(turns*2*math.pi, 1)).Operator()
helix_edge = BRepBuilderAPI_MakeEdge(slope, cyl).Edge()
helix = BRepBuilderAPI_MakeWire(helix_edge).Wire()

#what a fucking pain in the ass
circle = gp_Circ(gp_Ax2(gp_Pnt(radius,0,0), gp_Dir(0,1,0)), 0.05)
circle_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
circle_wire = BRepBuilderAPI_MakeWire(circle_edge).Wire()
circle_face = BRepBuilderAPI_MakeFace(circle_wire).Shape()



line_edge = BRepBuilderAPI_MakeEdge(gp_Pnt(radius,0,0), gp_Pnt(radius,0,1)).Edge()
line_wire = BRepBuilderAPI_MakeWire(line_edge).Wire()
line_edge = BRepBuilderAPI_MakeEdge(gp_Pnt(radius,0,0), gp_Pnt(radius,0,1)).Shape()

print helix.Closed()
print circle_edge.Closed()
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
sweep = BRepPrimAPI_MakePrism(circle_face, gp_Vec(0,1,0)).Shape()
#sweep = BRepOffsetAPI_MakePipe(helix, circle_edge).Shape()
#sweep = BRepOffsetAPI_MakePipe(circle_wire, line_edge).Shape()


helix_curve = BRep_Tool().Curve(helix_edge)[0] #wtf
circle_curve = BRep_Tool().Curve(circle_edge)[0]
#aPipe2 = GeomFill_Pipe(helix,TC1,TC2, mode)
print type(helix_curve)
aPipe2 = GeomFill_Pipe(helix_curve, circle_curve)
aPipe2.Perform(0,0)
aSurface2= aPipe2.Surface()


#ps = BRepOffsetAPI_MakePipeShell(helix)
#ps.Add(circle_wire)
#print 'hi'
#ps.SetMode(True)
#display.DisplayShape(ps.Generated(circle_wire).Last())
#display.DisplayShape(ps.FirstShape())
#print 'here'
#ps.Build()
#sweep = ps.MakeSolid()

display.DisplayShape(helix)
#display.DisplayShape(circle_face)
#display.DisplayShape(line_edge)
#display.DisplayShape(sweep)
start_display()
