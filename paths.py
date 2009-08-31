#process geometry framework
#provides code to interpret geometrical constraints and carry out random operations

import random, sys

from OCC.gp import *
from OCC.Geom2d import *
from OCC.Geom2dAdaptor import *
from OCC.Geom2dAPI import *
from OCC.GCPnts import *
from OCC.GC import *

from OCC.GccEnt import *
from OCC.GccAna import *
from OCC.Geom2dGcc import *
from OCC.GCE2d import *
from OCC.gce import *
from OCC.Precision import *
from OCC.Display.wxSamplesGui import display

import math #OCC.math gets in the way? wtf

import skdb
from geom import *
from gui import *

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

from copy import copy, deepcopy
from random import randint

#move most of this into the lego package
lego = skdb.load_package('lego'); lego.load_data()
current_brick = None
all_bricks = [] #not currently used

for brick in lego.parts:
    brick.load_CAD()

def get_brick():
    '''returns a basic lego brick part from the catalog (no side effects)'''
    brick = deepcopy(lego.parts[random.randint(0,len(lego.parts)-1)])
    brick = deepcopy(lego.parts[random.randint(2,2)])
    brick.post_init_hook()
    return brick

#not sure where to move this
def show_bricks():
    display.EraseAll()
    display.DisplayShape([brick.shapes[0] for brick in all_bricks])

def make_lego(event=None, brick=None):
    import math
    global current_brick, all_bricks
    if brick is None: brick = get_brick() #load a brick from the catalog
    current_brick = brick
    tmp = gp_Trsf()
    #give it an interesting starting orientation (not 0)
    tmp.SetTranslation(Point(0,0,0), Point(3.14, 3.14, 3.14))
    tmp.SetRotation(gp_Ax1(Point(0,0,0), Direction(1,0,0)), math.pi/3)
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
        opts = i1.options(brick2)
        if opts or n > 20: break
        brick2 = get_brick() #try again
        n+=1
    conn =opts[random.randint(0, len(opts)-1)]
    
    #i1 = current_brick.interfaces[3]
    #i2 = brick2.interfaces[7]
    #conn = skdb.Connection(i1, i2)

    trsf = mate_connection(conn)
    brick2.transformation = trsf
    #brick2.shapes[0] keeps on being overwritten. what's the point of having it be a list?
    brick2.shapes[0] = BRepBuilderAPI_Transform(brick2.shapes[0], trsf, True).Shape() #move it
    conn.interface1.show()
    print "%.2f %.2f %.2f" % Point(conn.interface1.point).Transformed(conn.interface1.part.transformation).Coord()
    conn.interface2.show()
    print "%.2f %.2f %.2f" %  Point(conn.interface2.point).Transformed(conn.interface2.part.transformation).Coord()

    all_bricks.append(brick2)
    display.DisplayShape(brick2.shapes[0])
    current_brick = brick2
    naive_coincidence_fixer()

current_brick = get_brick()
brick2 = get_brick()
opts = current_brick.options(brick2)
opt = 0

def naive_coincidence_fixer():
    '''this is slow because it compares every interface to every other interface.'''
    global all_bricks
    all_i = set()
    for brick in all_bricks:
        for i in brick.interfaces:
            all_i.add(i)
    for i in all_i:
        for j in all_i:
            if i is j: break
            ipt = Point(i.point).transformed(i.part.transformation)
            jpt = Point(j.point).transformed(j.part.transformation)
            if ipt == jpt: # and Direction(i.x_vec) == Direction(j.x_vec).Reversed():
                if i.connected and j.connected: break
                print "score!"
                Connection(i, j).connect()
                i.show(); j.show()
                
def clear(event=None):
    global current_brick, all_bricks
    current = None
    current_brick = None
    all_bricks=[]
    display.EraseAll()

def save(event=None):
    '''dump the current construction'''
    global all_bricks
    return

add_key('a', add_lego)
add_key('c', clear)
add_key('m', make_lego)
add_key('i', show_interfaces)
add_key(' ', show_next_mate)
add_key('v', save)

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
                    save,
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
        
