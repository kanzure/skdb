#process geometry framework
#provides code to interpret geometrical constraints and carry out random operations

import random, sys

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
from OCC.BRepAlgoAPI import *
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

import math #OCC.math gets in the way? wtf
import skdb
from geom import Point, Vector, Direction, Transformation, mate_connection, move_shape, point_shape, point_along, build_trsf

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



from copy import copy, deepcopy
from random import randint


lego = skdb.load_package('lego'); lego.load_data()
current_brick = None
all_bricks = [] #not currently used

def get_brick():
    brick = deepcopy(lego.parts[random.randint(0,len(lego.parts)-1)])
    #brick = deepcopy(lego.parts[random.randint(2,2)])
    brick.post_init_hook()
    brick.load_CAD()
    return brick

def show_bricks():
    display.EraseAll()
    display.DisplayShape([brick.shapes[0] for brick in all_bricks])

def make_lego(event=None, brick=None):
    global current_brick, all_bricks
    if brick is None: brick = get_brick()
    current_brick = brick
    tmp = gp_Trsf()
    tmp.SetTranslation(Point(0,0,0), Point(3.14, 3.14, 3.14))
    #orient the part so that i[0] is aligned with the origin's z-axis
    i = current_brick.interfaces[0]
    trsf = i.get_transformation().Inverted()
    trsf.Multiply(tmp.Inverted()) #side effect
    current_brick.transformation = trsf #side effect
    shapes = current_brick.shapes 
    shapes[0] = BRepBuilderAPI_Transform(shapes[0], trsf, True).Shape() #move it
    display.DisplayColoredShape(shapes[0], 'RED')
    all_bricks.append(current_brick)

def add_lego(event=None, brick=None):
    global current_brick, all_bricks
    opts = None
    n=0
    if brick is not None: brick2 = brick
    else: brick2 = get_brick()
    while True:
        i1 = current_brick.interfaces[random.randint(0, len(current_brick.interfaces)-1)]
        i1 = current_brick.interfaces[0]
        opts = list(i1.options(brick2))
        if opts or n > 20: break
        brick2 = get_brick() #try again
        n+=1
    conn =opts[random.randint(0, len(opts)-1)]
    
    #i1 = current_brick.interfaces[3]
    #i2 = brick2.interfaces[7]
    #conn = skdb.Connection(i1, i2)

    trsf = mate_connection(conn)
    brick2.transformation = trsf
    brick2.shapes[0] = BRepBuilderAPI_Transform(brick2.shapes[0], trsf, True).Shape() #move it
    print Point(current_brick.interfaces[0].point).Transformed(current_brick.transformation).Coord() #0,0,0
    conn.interface1.show()
    print "%.2f %.2f %.2f" % Point(conn.interface1.point).Transformed(conn.interface1.part.transformation).Coord()
    conn.interface2.show()
    print "%.2f %.2f %.2f" %  Point(conn.interface2.point).Transformed(conn.interface2.part.transformation).Coord()

    all_bricks.append(brick2)
    display.DisplayShape(brick2.shapes[0])
    current_brick = brick2

current_brick = get_brick()
brick2 = get_brick()
opts = list(current_brick.options(brick2))
opt = 0

def show_next_mate(event=None, mate=None):
    '''cycle through available options and display them with each keypress'''
    global opt
    display.EraseAll()
    display.DisplayColoredShape(current_brick.shapes[0], 'RED')
    conn=opts[opt]
    opt += 1
    trsf = mate_connection(conn)

    display.DisplayShape(BRepBuilderAPI_Transform(conn.interface2.part.shapes[0], trsf, True).Shape())
    display.DisplayShape(make_vertex(Point(conn.interface1.point).Transformed(trsf)))
    display.DisplayShape(make_vertex(Point(conn.interface2.point).Transformed(trsf)))
    
#TODO move to geom.py
def blarney(self):
        tmp = self.part.transformation
        tmp2 = self.get_transformation()
        trsf1 = tmp.Multiplied(tmp2)
        display.DisplayShape(make_vertex(Point(0,0,0).Transformed(trsf1)))
        display.DisplayShape(Arrow(scale=5).to(trsf1))
skdb.Interface.show = blarney

def show_interfaces(event=None, brick=None):
    if brick is None: brick = current_brick
    for i in brick.interfaces:
        i.show()

def make_arrow(event=None, origin=gp_Pnt(0,0,0), direction=gp_Dir(0,0,1), scale=1, text=None, color="YELLOW"):
    '''draw a small arrow from origin to dest, labeled with 2d text'''
    arrow = Arrow(origin=origin, direction=direction, scale=scale).Shape()
    display.DisplayColoredShape(arrow, color)
    if text is not None:
        make_text(text, origin, 6)

#TODO move to geom.py
class Arrow(TopoDS_Shape):
    def __init__(self, origin=gp_Pnt(0,0,0), direction=gp_Dir(0,0,1), scale=1):
        self.origin = Point(origin)
        self.direction = Direction(direction)
        self.scale = scale
        self.build_shape()
        #apparently this screws up later transformations somehow
        ##apparently we must translate and then rotate
        #tmp = gp_Trsf()
        #tmp.SetTranslation(gp_Pnt(0,0,0), origin)
        #self.transformation = tmp.Multiplied(point_along(direction))
        self.transformation = gp_Trsf()
        #self.to(tmp)

        #tmp = point_along(direction)
        #self.transformation.Multiply(tmp)
    def build_shape(self):
        scale = self.scale
        body = BRepPrimAPI_MakeCylinder(0.02*scale, 0.7*scale).Shape()
        head = BRepPrimAPI_MakeCone(0.1*scale,0.001,0.3*scale).Shape()
        head = move_shape(head, gp_Pnt(0,0,0), gp_Pnt(0,0,0.7*scale)) #move cone to top of arrow
        self._shape =  BRepAlgoAPI_Fuse(head, body).Shape()
        
    def Shape(self): 
        return BRepBuilderAPI_Transform(self._shape, self.transformation).Shape()
    
    def to(self, dest):
        assert isinstance(dest, gp_Trsf)
        self.transformation.Multiply(dest)
        return self.Shape()

class Flag(Arrow):
    def __init__(self, origin=gp_Pnt(0,0,0), direction=gp_Dir(0,0,1), scale=1):
        Arrow.__init__(self, origin=origin, direction=direction, scale=scale)
    def build_shape(self):
        scale = self.scale
        body = BRepPrimAPI_MakeCylinder(0.02*scale, 1*scale).Shape()
        head = BRepPrimAPI_MakeWedge (0.3*scale, 0.05*scale, 0.3*scale, 0.1).Shape() #dx, dy, dz, ltx(?)
        head = move_shape(head, gp_Pnt(0,0,0), gp_Pnt(0,0,0.7*scale)) #move flag to top of arrow
        self._shape = BRepAlgoAPI_Fuse(head, body).Shape()
        
def chain_arrows(event=None):
    #a silly chain of arrows
    make_arrow(origin=gp_Pnt(0,0,1), direction=gp_Dir(1,1,1))
    display.DisplayShape(make_vertex(gp_Pnt(1,1,2)))
    s=math.sqrt(3)/3
    make_arrow(origin=gp_Pnt(s,s,s+1), direction=gp_Dir(1,1,1), text='hmm')

def coordinate_arrow(direction, color='YELLOW', flag=False, scale=3):
    if flag: shape = Flag(scale=scale, direction=direction)
    else: shape = Arrow(scale=scale, direction=direction)
    display.DisplayColoredShape(shape.Shape(), color)

def coordinate_arrows(event=None):
    #typical origin symbol
    display.DisplayShape(make_vertex(gp_Pnt(0,0,0)))
    for (v, c) in [[(1,0,0), 'RED'], [(0,1,0), 'GREEN'], [(0,0,1), 'BLUE']]:
        coordinate_arrow(v, c)
        
def test_coordinate_arrows(event=None):
    for a in 0, 1, -1:
        for b in 0, 1, -1:
            for c in 0, 1, -1:
                try: coordinate_arrow([a, b, c], flag=True)
                except RuntimeError:
                    pass

def test_transformation(event=None):
    brick = get_brick()
    point = [10,10,10]
    colors = [ 'WHITE', 'BLUE', 'RED', 'GREEN', 'YELLOW',
                    'WHITE', 'BLUE', 'RED', 'GREEN', 'YELLOW',
                    'WHITE', 'BLUE', 'RED', 'GREEN', 'YELLOW']
    #testfile = '20vert.yaml'
    #testfile = '60horz.yaml'
    #testfile = '60twist.yaml'
    #testfile = '60all.yaml'
    #testfile = '90vert.yaml'
    #testfile = '90horz.yaml'
    testfile = '90twist.yaml'
    for (i, color) in zip(skdb.load(open(testfile)), colors):
        trsf = build_trsf(i.point, i.x_vec, i.y_vec)
        display.DisplayColoredShape(BRepBuilderAPI_Transform(brick.shapes[0], trsf).Shape(), color)

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
    global current_brick, all_bricks
    current = None
    current_brick = None
    all_bricks=[]
    display.EraseAll()

def exit(event=None):
    sys.exit() 


from pymates import add_key
add_key('a', add_lego)
add_key('c', clear)
add_key('m', make_lego)
add_key('i', show_interfaces)
add_key(' ', show_next_mate)

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
                    chain_arrows,
                    coordinate_arrows,
                    test_coordinate_arrows,
                    show_interfaces,
                    make_lego,
                    add_lego,
                    clear,
                    exit
                    ]:
            add_function_to_menu('demo', f)
        #random_sweep()
        init_display()
        make_lego()
        add_lego()
        coordinate_arrows()
        #test_transformation()
        start_display()

        
