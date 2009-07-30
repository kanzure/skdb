#process geometry framework
#provides code to interpret geometrical constraints and carry out random operations

import random, sys, math

from OCC.gp import *
from OCC.Geom2d import *
from OCC.Geom2dAdaptor import *
from OCC.Geom2dAPI import *
from OCC.GCPnts import *
from OCC.GC import *

# for make_text
from OCC.BRepPrimAPI import *
from OCC.BRepBuilderAPI import *
from OCC.BRepFilletAPI import *
from OCC.BRepOffsetAPI import *
from OCC.BRep import *
from OCC.TopExp import *
from OCC.TopAbs import *
from OCC.TopoDS import *
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

current = gp_Pnt2d(0,0)

def random_line(scale=10):
    global current
    p1 = current  #should be a gp_Pnt2d
    p2 = gp_Pnt2d(random.randint(0, scale), random.randint(0, scale))
    v2 = gp_Vec2d(p1, p2)
    current = p1.Translated(v2)
    return GCE2d_MakeSegment(p1, p2).Value()

def random_arc(scale=10):
    global current
    p1 = current  #should be a gp_Pnt2d
    p2 = gp_Pnt2d(random.randint(0, scale), random.randint(0, scale))
    p3 = gp_Pnt2d(random.randint(0, scale), random.randint(0, scale))
    v3 = gp_Vec2d(p1, p3)
    current = p1.Translated(v3)
    return GCE2d_MakeArcOfCircle(p1, p2, p3).Value()

def draw_random_line(event=None):
    display.DisplayShape([make_edge2d(random_line())])

def draw_random_arc(event=None):
    display.DisplayShape([make_edge2d(random_arc())])

def line_arc_line_path(event=None):
    radius = 10
    mkwire =  BRepBuilderAPI_MakeWire()
    print "create edges"
    for i in range(3):
        edge = BRepBuilderAPI_MakeEdge2d(random_line()).Edge()
        mkwire.Add(edge)
    wire = mkwire.Wire()
    print "create face"
    face = BRepBuilderAPI_MakeFace(wire).Face()
    fillet = BRepFilletAPI_MakeFillet2d(face)
    #print fillet.Status()
    print "explore face"
    explorer = TopExp_Explorer(face, TopAbs_VERTEX)
    i=0
    while explorer.More():
        print "vertex: ", i
        vertex = TopoDS().Vertex(explorer.Current())
        make_vertex(BRep_Tool().Pnt(vertex))
        #help( vertex.Location().Value())
        fillet.AddFillet(vertex, radius)
        fillet.Build()
        print fillet.NbFillet()
        #print fillet.IsDone()
        #while not fillet.IsDone(): pass
        explorer.Next()
        i+=1

    display.DisplayShape([face])
    return wire
    
def random_cone(event=None):
    #p1, p2, p3, p4 = None, None, None, None #ew
    #for i in p1, p2, p3, p4:
        #i = gp_Pnt(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
        #print i.Coord()
    p1 = gp_Pnt(0,0,0)
    p2 = gp_Pnt(0,0,1)
    p3 = 1
    p4 = 2
    cone = gce_MakeCone(p1, p2, p3, p4).Value()
    cone = BRepPrimAPI_MakeCone(gp.gp().XOY(), 1,1.1,1)
    try: 
        cone = BRepPrimAPI_MakeCone(gp.gp().XOY(), random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)).Shape()
        display.DisplayShape([cone])
    except RuntimeError: cone = random_cone()
    return cone
    
def sweep_path(path, shape):
    print type(shape)
    print type(path)
    assert type(shape) == TopoDS_Shape
    #assert type(path) == TopoDS_Wire #bah
    sweep = BRepOffsetAPI_MakePipe(path, shape).Shape()
    return sweep
    
def random_sweep(event=None):
    display.DisplayShape([sweep_path( line_arc_line_path(), random_cone())])
    

##bandsaw tomfoolery
#path = []
#done = False
#while not done:
    #path += random_line(current)
    #path += random_arc(current)

def make_edge2d(shape):
    spline = BRepBuilderAPI_MakeEdge2d(shape)
    spline.Build()
    return spline.Edge()

def make_edge(shape):
    spline = BRepBuilderAPI_MakeEdge(shape)
    spline.Build()
    return spline.Edge()

def make_vertex(pnt):
    if isinstance(pnt, gp.gp_Pnt2d):
        vertex = BRepBuilderAPI_MakeVertex( gp_Pnt(pnt.X(), pnt.Y(), 0))
    else: 
        vertex = BRepBuilderAPI_MakeVertex( pnt )
    vertex.Build()
    return vertex.Vertex()

def make_face(shape):
    face = BRepBuilderAPI_MakeFace(shape)
    face.Build()
    return face.Face()

def make_text(string, pnt, height):
    '''render a bunch of text at pnt's location
    myGroup should be an OCC.Graphic3d.Graphic3d_Group instance.
    call init_display before calling this function.
    '''
    global display
    _string = TCollection_ExtendedString(string)
    if isinstance( pnt, gp.gp_Pnt2d):
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), 0)
    else:
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), pnt.Z())
    myGroup.Text(_string, _vertex, height)

def move_shape(shape, from_pnt, to_pnt):
    trsf = gp_Trsf()
    trsf.SetTranslation(from_pnt, to_pnt)
    return BRepBuilderAPI_Transform(shape, trsf, True).Shape()

def angle_to(x,y,z):                                                         
    '''returns polar coordinates in radians to a point from the origin            
    a rotates around the x-axis; b rotates around the y axis; r is the distance'''
    azimuth = math.atan2(y, x) #longitude                                       
    elevation = math.atan2(z, math.sqrt(x**2 + y**2))                              
    radius = math.sqrt(x**2+y**2+z**2)                                                 
    return((azimuth, elevation, radius))  
    #glRotatef(az-90,0,0,1)                                                        
    #glRotatef(el-90,1,0,0) 

def point_shape(shape, origin):
    '''rotates a shape to point along origin's direction. this function ought to be unnecessary'''
    assert type(origin) == gp_Ax1
    #ox, oy, oz = origin.Location().X(), origin.Location().Y(), origin.Location().Z() #ffs
    ox, oy, oz = 0, 0, 0
    dx, dy, dz = origin.Direction().X(), origin.Direction().Y(), origin.Direction().Z()
    (az, el, rad) = angle_to(dx-ox, dy-oy, dz-oz)
    print "az: %s, el: %s, rad: %s... dx: %s, dy: %s, dz %s)" % (az, el, rad, dx, dy, dz)
    trsf = gp_Trsf()
    #this may be in backwards order?
    trsf.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(1,0,0)), el-math.pi/2)
    shape = BRepBuilderAPI_Transform(shape, trsf, True).Shape()
    trsf.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), az-math.pi/2)
    shape = BRepBuilderAPI_Transform(shape, trsf, True).Shape()

    return shape
    
    
def make_arrow(event=None, origin=gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), scale=1, text=None, color="YELLOW"):
    '''draw a small arrow from origin to dest, labeled with 2d text'''
    assert type(origin) == gp_Ax1
    body = BRepPrimAPI_MakeCylinder(0.05, 0.7).Shape()
    head = BRepPrimAPI_MakeCone(0.1,0.001,0.3).Shape()
    head = move_shape(head, gp_Pnt(0,0,0), gp_Pnt(0,0,0.7)) #move cone to top of arrow
    #arrow = BRepAlgoAPI_Fuse(head, body).Shape()
    head = point_shape(head, origin)
    body = point_shape(body, origin)
    head = move_shape(head, gp_Pnt(0,0,0), origin.Location())
    body = move_shape(body, gp_Pnt(0,0,0), origin.Location())

    display.DisplayColoredShape(head, color)
    display.DisplayColoredShape(body, color)

    
def make_arrow_to(dest=gp_Ax1(gp_Pnt(0,0,1), gp_Dir(0,0,1)), scale=1, text=None):
    pass

def init_display():
    '''The reason for recreating is that myGroup is gone after an EraseAll call'''
    global myGroup
    global myPresentation
    # now we have to make a presenation for a stupid sphere as a workaround to get to the object
    stupid_sphere = BRepPrimAPI_MakeSphere(1,1,1,1)
    prs_sphere = AIS_Shape(stupid_sphere.Shape())   
    d_ctx           = display.GetContext().GetObject()
    prsMgr          = d_ctx.CollectorPrsMgr().GetObject()
    d_ctx.Display(prs_sphere.GetHandle(), 1)
    myPresentation   = prsMgr.CastPresentation(prs_sphere.GetHandle()).GetObject()
    myGroup = Prs3d_Root().CurrentGroup(myPresentation.Presentation()).GetObject()


def tangents(curve1, curve2, radius=2):
    '''only works for lines and circles atm'''
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

def draw_all_tangents(event=None):
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
    L_gp = gce_MakeLin2d(points[3], points[4]).Value() #yuck. same thing; tangent solver wants a line, not segment
    
    tangents(C_gp, L_gp, radius=2)

def clear(event=None):
    display.EraseAll()

def exit(event=None):
    sys.exit() 

if __name__ == '__main__':
        from OCC.Display.wxSamplesGui import add_function_to_menu, add_menu, start_display
        add_menu('demo')
        for f in [
                    draw_all_tangents,
                    draw_random_line,
                    draw_random_arc,
                    line_arc_line_path,
                    random_cone,
                    random_sweep,
                    make_arrow,
                    clear,
                    exit
                    ]:
            add_function_to_menu('demo', f)
        #random_sweep()
        init_display()
        #a silly chain of arrows
        make_arrow(origin=gp_Ax1(gp_Pnt(0,0,1), gp_Dir(1,1,1)))
        display.DisplayShape(make_vertex(gp_Pnt(1,1,2)))
        s=math.sqrt(3)/3
        make_arrow(origin=gp_Ax1(gp_Pnt(s,s,s+1), gp_Dir(1,1,1)))
        #typical origin symbol
        display.DisplayShape(make_vertex(gp_Pnt(1,0,0)))
        make_arrow(color='RED', origin=gp_Ax1(gp_Pnt(0,0,0), gp_Dir(1,0,0)))
        make_arrow(color='GREEN', origin=gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,1,0)))
        make_arrow(color='BLUE', origin=gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)))
        
        start_display()
        
