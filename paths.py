#process geometry framework
#provides code to interpret geometrical constraints and carry out random operations

import random, sys

from OCC.gp import *
from OCC.Geom2d import *
from OCC.Geom2dAdaptor import *
from OCC.Geom2dAPI import *
from OCC.GCPnts import *


# for make_text
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *
from OCC.AIS import *
from OCC.Prs3d import *
from OCC.TCollection import *
from OCC.Graphic3d import *

from OCC.GccEnt import *
from OCC.GccAna import *
from OCC.Geom2dGcc import *
from OCC.GCE2d import *
from OCC.gce import *
from OCC.Precision import *
from OCC.Display.wxSamplesGui import display

#def arc():
    #pass

#current = (0,0)

##bandsaw tomfoolery
#path = []
#done = False
#while not done:
    #path += random_line(current)
    #path += random_arc(current)


def make_edge2d(shape):
    spline = BRepBuilderAPI_MakeEdge2d(shape)
    spline.Build()
    return spline.Shape()

def make_edge(shape):
    spline = BRepBuilderAPI_MakeEdge(shape)
    spline.Build()
    return spline.Shape()

def make_vertex(pnt):
    if isinstance(pnt, gp.gp_Pnt2d):
        vertex = BRepBuilderAPI_MakeVertex( gp_Pnt(pnt.X(), pnt.Y(), 0))
    else: 
        vertex = BRepBuilderAPI_MakeVertex( pnt )
    vertex.Build()
    return vertex.Shape()

def make_face(shape):
    face = BRepBuilderAPI_MakeFace(shape)
    face.Build()
    return face.Shape()


def make_text(string, pnt, height):
    '''render a bunch of text at pnt's location
    myGroup should be an OCC.Graphic3d.Graphic3d_Group instance; call init_display first
    '''
    global display
    _string = TCollection_ExtendedString(string)
    if isinstance( pnt, gp.gp_Pnt2d):
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), 0)
    else:
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), pnt.Z())
    myGroup.Text(_string, _vertex, height)

def init_display():
    '''The reason for recreating is that myGroup is gone after an EraseAll call'''
    global myGroup
    # now we have to make a presenation for a stupid sphere as a workaround to get to the object
    stupid_sphere = BRepPrimAPI_MakeSphere(1,1,1,1)
    prs_sphere = AIS_Shape(stupid_sphere.Shape())   
    d_ctx           = display.GetContext().GetObject()
    prsMgr          = d_ctx.CollectorPrsMgr().GetObject()
    d_ctx.Display(prs_sphere.GetHandle(), 1)
    aPresentation   = prsMgr.CastPresentation(prs_sphere.GetHandle()).GetObject()
    myGroup = Prs3d_Root().CurrentGroup(aPresentation.Presentation()).GetObject()


def tangents(curve1, curve2, radius=2):
    '''only works for lines and circles atm'''
    print type(curve1), type(curve2)
    #if type(curve1) == gp_Lin2d:
    QC = GccEnt.GccEnt().Unqualified(curve1)
    QL = GccEnt.GccEnt().Unqualified(curve2)
    TR = GccAna_Circ2d2TanRad(QC,QL,radius,Precision().Confusion())
    
    #TR = Geom2dGcc_Lin2d2Tan(QC, QL, Precision().Confusion()) #curve, curve, tol; or curve, point, tol
    def find_solns(TR):
        if TR.IsDone():
            NbSol = TR.NbSolutions()
            solutions = []
            for k in range(1,NbSol+1):
                circ = TR.ThisSolution(k)
                display.DisplayShape(make_edge2d(circ))
                # find the solution circle ( index, outvalue, outvalue, gp_Pnt2d )
                pnt1 = gp_Pnt2d()
                # find the first tangent point       
                parsol,pararg = TR.Tangency1(k, pnt1)  #gross      
                display.DisplayShape(make_vertex(pnt1))
                
                pnt2 = gp_Pnt2d()
                # find the second tangent point     
                parsol,pararg = TR.Tangency2(k, pnt2)
                display.DisplayShape(make_vertex(pnt2))
                solutions += (circ, pnt1, pnt2)
            return solutions
        else:
            print "TR didnt finish!"
            return

    find_solns(TR)

def line_arc_line_path(event=None):
    display.EraseAll()
    init_display()
    points = []
    for i in range(5):
        point = gp_Pnt2d(random.randint(0,10), random.randint(0,10))
        points += [point]
        make_text('P'+str(i), point, 6)
        display.DisplayShape(make_vertex(point))
    
    C = GCE2d_MakeArcOfCircle(points[0], points[1], points[2]).Value()
    display.DisplayShape(make_edge2d(C))
    C_gp = gce_MakeCirc2d(points[0], points[1], points[2]).Value() #ew. same thing; tangent solver wants a circle, not arc

    L = GCE2d_MakeSegment(points[3], points[4]).Value()
    #L = GccAna_Lin2d2Tan(points[3], points[4],Precision().Confusion()).ThisSolution(1)
    display.DisplayShape([make_edge2d(L)])
    print type(points[3]), type(points[4])
    L_gp = gce_MakeLin2d(points[3], points[4]).Value() #yuck. same thing; tangent solver wants a line, not segment
    
    tangents(C_gp, L_gp, radius=2)

def exit(event=None):
    sys.exit() 

if __name__ == '__main__':
        from OCC.Display.wxSamplesGui import add_function_to_menu, add_menu, start_display
        add_menu('demo')
        for f in [
                    line_arc_line_path,
                    exit
                    ]:
            add_function_to_menu('demo', f)
        line_arc_line_path()
        start_display()
