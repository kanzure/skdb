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
    '''
    render a bunch of text
    @param string: string to be rendered
    @param pnt:    location of the string
    @param myGroup:OCC.Graphic3d.Graphic3d_Group instance
    @param height: max height
    '''
    global display
    # returns a Handle_Visual3d_ViewManager instance
    # the only thing is that you need the Visual3d class to make this work well
    # now we have to make a presenation for a stupid sphere as a workaround to get to the object
#    viewer = display.GetContext().GetObject().CurrentViewer().GetObject().Viewer()
#    hstruct = Graphic3d_Structure(viewer)

#===============================================================================
#    STOOPID!!
#     The reason for recreating is that myGroup is gone after an EraseAll call
#===============================================================================
    stupid_sphere = BRepPrimAPI_MakeSphere(1,1,1,1)
    prs_sphere = AIS_Shape(stupid_sphere.Shape())   
    d_ctx           = display.GetContext().GetObject()
    prsMgr          = d_ctx.CollectorPrsMgr().GetObject()
    d_ctx.Display(prs_sphere.GetHandle(), 1)
    aPresentation   = prsMgr.CastPresentation(prs_sphere.GetHandle()).GetObject()
    global myGroup
    myGroup = Prs3d_Root().CurrentGroup(aPresentation.Presentation()).GetObject()
#===============================================================================
#    FINE
#===============================================================================
    _string = TCollection_ExtendedString(string)
    if isinstance( pnt, gp.gp_Pnt2d):
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), 0)
    else:
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), pnt.Z())
    myGroup.Text(_string, _vertex, height)

def circles2d_from_curves(event=None):
    display.EraseAll()
    points = []
    for i in range(5):
        point = gp_Pnt2d(random.randint(0,10), random.randint(0,10))
        points += [point]
        make_text('P'+str(i), point, 6)
        display.DisplayShape(make_vertex(point))
    
    C = gce_MakeCirc2d(points[0], points[1], points[2]).Value()

    display.DisplayShape(make_edge2d(C))
    
    QC = GccEnt.GccEnt().Outside(C)
                                                  
    L = GccAna_Lin2d2Tan(points[3], points[4],Precision().Confusion()).ThisSolution(1)
    display.DisplayShape([make_edge2d(GCE2d_MakeSegment(L, -2, 20).Value())])

    QL = GccEnt.GccEnt().Unqualified(L)
    radius = 2
    TR = GccAna_Circ2d2TanRad(QC,QL,radius,Precision().Confusion())
    
    #TR = Geom2dGcc_Lin2d2Tan(QC, QL, Precision().Confusion()) #curve, curve, tol; or curve, point, tol
     
    if TR.IsDone():
        NbSol = TR.NbSolutions()
        for k in range(1,NbSol+1):
            circ = TR.ThisSolution(k)
            display.DisplayShape(make_edge2d(circ))
            # find the solution circle ( index, outvalue, outvalue, gp_Pnt2d )
            pnt1 = gp_Pnt2d()
            parsol,pararg = TR.Tangency1(k, pnt1)  #gross
            # find the first tangent point                                    
            pnt2 = gp_Pnt2d()
            parsol,pararg = TR.Tangency2(k, pnt2)
            # find the second tangent point     
            pnt3 = gp_Pnt2d()                         
            parsol,pararg = TR.Tangency1(k, pnt3)
            # find the first tangent point                                    
            display.DisplayShape(make_vertex(pnt3))#,"tangentpoint1",0,0.1,0,0.05)
            #make_text("tangentpoint1", pnt3, 6)
            
            pnt4 = gp_Pnt2d()                         
            parsol,pararg = TR.Tangency2(k, pnt4)
            display.DisplayShape(make_vertex(pnt4))
            #display.DisplayPoint(pnt4,"tangentpoint2",0,0.1,0,0.05)
            #make_text("tangentpoint2", pnt4, 6)
            # find the second tangent point                                         
    else:
        print "TR didnt finish!"
        return

def exit(event=None):
    sys.exit() 

if __name__ == '__main__':
        from OCC.Display.wxSamplesGui import add_function_to_menu, add_menu, start_display
        add_menu('demo')
        for f in [
                  circles2d_from_curves,
                  exit
                  ]:
            add_function_to_menu('demo', f)
        circles2d_from_curves()
        start_display()
