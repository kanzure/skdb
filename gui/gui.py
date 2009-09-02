#!/usr/bin/python
import sys
from OCC.gp import *
from OCC.TopoDS import *
from OCC.BRepBuilderAPI import *
from OCC.BRepPrimAPI import *
from OCC.BRepAlgoAPI import *
from OCC.AIS import *
from OCC.Graphic3d import *
from OCC.Prs3d import *
from OCC.TCollection import *
from OCC.Display.wxSamplesGui import add_function_to_menu, add_menu, start_display, display
import OCC.Display.wxSamplesGui
from skdb.geom import Point, Direction, move_shape, point_along
from skdb import Interface

class Arrow(TopoDS_Shape):
    def __init__(self, origin=gp_Pnt(0,0,0), direction=gp_Dir(0,0,1), scale=1):
        self.origin = Point(origin)
        self.direction = Direction(direction)
        self.scale = scale
        self.build_shape()
        #apparently this screws up later transformations somehow
        ##apparently we must translate and then rotate
        tmp = gp_Trsf()
        tmp.SetTranslation(gp_Pnt(0,0,0), origin)
        #self.transformation = tmp.Multiplied(point_along(direction))
        self.transformation = gp_Trsf()
        self.to(point_along(direction))
        self.to(tmp)


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

def show_interfaces(event=None, brick=None):
    if brick is None: brick = current_brick
    for i in brick.interfaces:
        i.show()

def show_interface_arrow(self, color=None):
        tmp = self.part.transformation
        tmp2 = self.get_transformation()
        trsf1 = tmp.Multiplied(tmp2)
        arrow = Arrow(scale=5)
        arrow.transformation = trsf1
        if color:
            display.DisplayColoredShape(make_vertex(Point(0,0,0).Transformed(trsf1)), color)
            display.DisplayColoredShape(arrow.Shape(), color)
        else:
            display.DisplayShape(make_vertex(Point(0,0,0).Transformed(trsf1)))
            display.DisplayShape(arrow.Shape())

Interface.show = show_interface_arrow

def make_text(string, pnt, height):
    '''render a bunch of text at pnt's location
    myGroup should be an OCC.Graphic3d.Graphic3d_Group instance.
    call init_display before calling this function.
    '''
    global display
    _string = TCollection_ExtendedString(string)
    if isinstance( pnt, gp_Pnt2d):
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), 0)
    else:
        _vertex = Graphic3d_Vertex(pnt.X(), pnt.Y(), pnt.Z())
    myGroup.Text(_string, _vertex, height)

def make_arrow(event=None, origin=gp_Pnt(0,0,0), direction=gp_Dir(0,0,1), scale=1, text=None, color="YELLOW"):
    '''draw a small arrow from origin to dest, labeled with 2d text'''
    arrow = Arrow(origin=origin, direction=direction, scale=scale).Shape()
    display.DisplayColoredShape(arrow, color)
    if text is not None:
        make_text(text, origin, 6)

def coordinate_arrow(direction, color='YELLOW', flag=False, scale=3):
    if flag: shape = Flag(scale=scale, direction=direction).Shape()
    else: shape = Arrow(scale=scale, direction=direction).Shape()
    display.DisplayColoredShape(shape, color)

def coordinate_arrows(event=None):
    #typical origin symbol
    display.DisplayShape(make_vertex(gp_Pnt(0,0,0)))
    for (v, c) in [[(1,0,0), 'RED'], [(0,1,0), 'GREEN'], [(0,0,1), 'BLUE']]:
        coordinate_arrow(v, c)

def chain_arrows(event=None):
    #a silly chain of arrows
    make_arrow(origin=gp_Pnt(0,0,1), direction=gp_Dir(1,1,1))
    display.DisplayShape(make_vertex(gp_Pnt(1,1,2)))
    s=math.sqrt(3)/3
    make_arrow(origin=gp_Pnt(s,s,s+1), direction=gp_Dir(1,1,1), text='hmm')

def add_key(key,method_to_call,**keywords):
    '''binds a key to a particular method
    ex: add_key("G",some_method)
    '''
    import functools
    upper_case = key.upper()
    orded = ord(upper_case) #see wxDisplay.py line 171
    OCC.Display.wxSamplesGui.frame.canva._key_map[orded] = functools.partial(method_to_call, keywords)
    print "added a key with name = ", orded, " mapped to method = ", method_to_call
    return

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

def clear(event=None):
    display.EraseAll()

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


def make_vertex(pnt):
    if isinstance(pnt, gp_Pnt2d):
        vertex = BRepBuilderAPI_MakeVertex( gp_Pnt(pnt.X(), pnt.Y(), 0))
    else:
        vertex = BRepBuilderAPI_MakeVertex( pnt )
    vertex.Build()
    return vertex.Vertex()

def exit(event=None):
    sys.exit()

