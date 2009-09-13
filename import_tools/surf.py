#!/usr/bin/python
#############################
#put insightful overview here
#############################
from copy import copy, deepcopy
import unittest

#in case i do something stupid and it hangs..
from os import getpid
print "*** pid = ", getpid()

#let's not reinvent the wheel
from skdb import Point

#stuff that actually matters
import OCC.TopoDS as TopoDS
from OCC.TopoDS import TopoDS_Vertex
from OCC.TColgp import TColgp_Array1OfPnt, TColgp_Array2OfPnt
from OCC.GeomAPI import GeomAPI_PointsToBSplineSurface, GeomAPI_PointsToBSpline
from OCC.GeomAdaptor import GeomAdaptor_HCurve
from OCC.GeomFill import GeomFill_SimpleBound
from OCC.Geom import Handle_Geom_BSplineSurface, Geom_BSplineSurface
from OCC.GeomPlate import GeomPlate_BuildPlateSurface, GeomPlate_PointConstraint, GeomPlate_MakeApprox
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon
from OCC.BRepAdaptor import BRepAdaptor_HCurve
from OCC.BRepFill import BRepFill_CurveConstraint
from OCC.Utils.Topology import WireExplorer
from OCC.TopExp import TopExp_Explorer
from OCC.TopAbs import TopAbs_VERTEX, TopAbs_FACE
from OCC.Utils.DataExchange.STL import STLImporter
from OCC.BRep import BRep_Tool

#gui stuff
from skdb.gui import *

#points = TColgp_Array2OfPnt()
#surface = GeomAPI.GeomAPI_PointsToBSplineSurface(points) #surface is of type GeomAPI_PointsToBSplineSurface
#surface1 = surface.Surface() #surface1 is of type Handle_Geom_BSplineSurface
####surface2 = surface1.GetObject() #surface2 is of type Geom_BSplineSurface
#surface2 = Handle_Geom_Surface(surface1)
#face = BRepBuilderAPI_MakeFace(surface2)
#my_shape = face.Shape()
#OCC.Display.wxSamplesGui.display.DisplayShape(my_shape)

def point_list_to_TColgp_Array1OfPnt(li):
    pts = TColgp_Array1OfPnt(0, len(li)-1)
    for n,i in enumerate(li):
        pts.SetValue(n,i)
    return pts
#not that anyone is going to remember that..
point_list_1 = point_list_to_TColgp_Array1OfPnt

#this doesnt work
def point_list_to_TColgp_Array2OfPnt(li):
    assert (len(li))%2 == 0, "point_list_to_TColgp_Array2OfPnt: the length of the list must be divisible by two so it can be split into two."
    pts = TColgp_Array2OfPnt(0, (len(li)-1)/2, 0, (len(li)-1)/2)
    print "row_length: ", pts.RowLength()
    print "column_length: ", pts.ColLength()
    first_half = li[:len(li)/2]
    second_half = li[len(li)/2:]
    for n,i in enumerate(first_half):
        print "n, i = (%s, %s)" % (n, i)
        pts.SetValue(0,n,i) #row, column, value
    for n,i in enumerate(second_half):
        pts.SetValue(1,n,i)
    print "done"
    return pts
#synonym
point_list_2 = point_list_to_TColgp_Array2OfPnt

def get_simple_bound(rndPts0):    
    _spl1 = GeomAPI_PointsToBSpline(rndPts0) #not a GeomAPI_PointsToBSplineSurface ??
    _spl1.thisown = False
    spl1  = _spl1.Curve()
    
    spl1_adap = GeomAdaptor_HCurve(spl1)
    spl1_adap.thisown = False
    spl1_adap_h = spl1_adap.GetHandle()
    bound1 = GeomFill_SimpleBound(spl1_adap_h, 0.001, 0.001)
    bound1.thisown = False
    bound1_h = bound1.GetHandle()
    return spl1, bound1_h

def build_plate(polygon, points):
    ''' 
    build a surface from a constraining polygon(s) and point(s)
    @param polygon:     list of polygons ( TopoDS_Shape)
    @param points:      list of points ( gp_Pnt ) 
    '''
    # plate surface
    bpSrf = GeomPlate_BuildPlateSurface(3,15,2)
    
    # add curve constraints
    for poly in polygon:
        for edg in WireExplorer(poly.Wire()).ordered_edges():
            c = BRepAdaptor_HCurve()
            c.ChangeCurve().Initialize(edg)
            constraint = BRepFill_CurveConstraint(c.GetHandle(), 0)
            bpSrf.Add(constraint.GetHandle())
     
    # add point constraint
    for pt in points:
        bpSrf.Add(GeomPlate_PointConstraint(pt, 0).GetHandle())
        bpSrf.Perform()
    
    maxSeg, maxDeg, critOrder = 9,8,0
    tol  = 1e-4
    dmax = max([tol,10*bpSrf.G0Error()])
    
    srf = bpSrf.Surface()
    plate = GeomPlate_MakeApprox(srf, tol, maxSeg, maxDeg, dmax, critOrder)
    
    uMin, uMax, vMin, vMax = srf.GetObject().Bounds()
    
    face = BRepBuilderAPI_MakeFace(plate.Surface(), uMin, uMax, vMin, vMax)
    face.Build()
    return face

#this doesnt work, see build_plate instead
def approximate_surface(points=[]):
    #just to be safe, let's convert that list to Point objects
    if points is not []:
        new_points = []
        for point in points:
            if not isinstance(point, Point):
                new_points.append(gp_Pnt(Point(point)._CSFDB_Getgp_Pntcoord()))
            else: new_points.append(point)
        points = new_points
    points = point_list_2(points)
    print "approximate_surface: about to call GeomAPI_PointsToBSplineSurface"
    surface = GeomAPI_PointsToBSplineSurface(points)
    print "approximate_surface: about to call surface.Surface"
    surface1 = surface.Surface()
    surface2 = Handle_Geom_Surface(surface1)
    print "approximate_surface: about to call BRepBuilderAPI_MakeFace"
    face = BRepBuilderAPI_MakeFace(surface2)
    #to get a TopoDS_Face, do: face.Face()
    my_shape = face.Shape()
    print "approximate_surface: returning"
    return my_shape

class Cloud:
    '''a cloud of points in 3D space'''
    def __init__(self, points=[]):
        self._points = points
        pass
    def __add__(self, other):
        '''implements what is known as "registration" (actually not yet)'''
        if isinstance(other, Point):
            #add the point to the cloud
            #FIXME: need to express this point in the common coordinate system ("registration")
            temp = copy(self)
            temp._points.append(other)
            return temp
        elif isinstance(other, Cloud):
            #merge these two clouds
            #FIXME: align the two coordinate systems
            points = copy(self._points)
            points.append(copy(other._points))
            temp = Cloud(points=points)
            return temp

class Surface:
    def __init__(self):
        self.bottom_left, self.bottom_right, self.top_left, self.top_right = Point(0,0,0), Point(0,0,0), Point(0,0,0), Point(0,0,0)
        self.points = [] #points that we want to approximate
        self.shape = TopoDS_Shape()
        self.polygons = [BRepBuilderAPI_MakePolygon()]
    def make_bounding_box(self):
        '''figures out a bounding box from a set of points.
        this is just to set bottom_left, top_right, bottom_right, top_left
        see Surface.approximate for the real magic.'''
        x_list, y_list, z_list = [], [], []
        #really we just need to figure out two points
        for point in self.points:
            x, y, z = point.Coord()
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
        x_min, y_min, z_min = min(x_list), min(y_list), min(z_list)
        x_max, y_max, z_max = max(x_list), max(y_list), max(z_list)
        #we're assuming z=0 for this plane that we're working on.
        #check to make sure the points line up in the z=0 plane
        self.bottom_left = Point(x_min, y_min, 0)
        self.top_right = Point(x_max, y_max, 0)
        self.bottom_right = Point(x_max, y_min, 0)
        self.top_left = Point(x_min, y_max, 0)
    def approximate(self):
        '''make a boundary representation of a surface that approximates the points'''
        self.make_bounding_box()
        #make the bounding box into a polygon
        poly = BRepBuilderAPI_MakePolygon()
        map(poly.Add, [self.bottom_left, self.bottom_right, self.top_left, self.top_right])
        poly.Build()
        self.polygons = [poly]
        my_surf = build_plate(self.polygons, self.points)
        self.shape = my_surf.Shape()
        display.DisplayShape(self.shape)

app = Surface()

def make_point(vertex):
    #print "make_point: vertex=", vertex
    if isinstance(vertex, TopoDS_Vertex):
        return Point(BRep_Tool().Pnt(vertex))
    else: return vertex

def load_stl(filename):
    '''load_stl(filename) -> TopoDS_Shape'''
    importer = STLImporter(filename)
    importer.ReadFile()
    shape = importer.GetShape()
    return shape

def extract_shape_vertices(shape):
    '''dumps a list of points that define the shape'''
    faces = []
    all_vertices = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = TopoDS().Face(explorer.Current())
        faces.append(face)
        vertices = process_face(face)
        all_vertices.append(vertices)
        explorer.Next()
    return all_vertices

def process_face(face):
    '''dumps a list of points that define the face'''
    vertices = []
    explorer = TopExp_Explorer(face, TopAbs_VERTEX)
    while explorer.More():
        vertex = TopoDS().Vertex(explorer.Current())
        vertices.append(vertex)
        explorer.Next()
    return vertices

def demo(event=None):
    global app
    app.approximate()

def clear(event=None):
    global app
    app = Surface() #start over again
    display.EraseAll()

def ask_user(event=None):
    global app
    x = raw_input("x?")
    y = raw_input("y?")
    z = raw_input("z?")
    app.points.append(Point(x,y,z))

def exit_app(event=None):
    sys.exit()

add_key("c", clear)
add_key("a", ask_user)
add_key("d", demo)

pts = [Point(0,0,0), Point(0,0,1), Point(0,1,0), Point(0,1,1), Point(1,0,0), Point(1,1,0), Point(1,0,1), Point(1,1,1)]
class TestApproximation(unittest.TestCase):
    def test_point_list(self):
        tcolgp_array = point_list_1(pts)
        self.assertTrue(isinstance(tcolgp_array, TColgp_Array1OfPnt))
        tcolgp_array = point_list_2(pts)
        self.assertTrue(isinstance(tcolgp_array, TColgp_Array2OfPnt))
    def test_approximate(self):
        #my_surface = approximate_surface(pts)
        p1,p2,p3,p4,p5 = Point(0,0,0),Point(0,10,0),Point(0,10,10),Point(0,0,10),Point(5,5,5)
        poly = BRepBuilderAPI_MakePolygon()
        map(poly.Add, [p1,p2,p3,p4,p1])
        poly.Build()
        
        my_surf = build_plate([poly], [Point(-1,-1,-1)])
        sh = my_surf.Shape()
        display.DisplayShape(sh)
    def test_stl(self):
        #shape = load_stl("/home/kanzure/local/pythonocc-0.3/pythonOCC/src/samples/Level2/DataExchange/sample.stl")
        shape = load_stl("/home/kanzure/code/skdb/import_tools/blah.stl")
        #shape = load_stl("/home/kanzure/local/legos/diver.stl")
        display.DisplayShape(shape)
        temp_points = extract_shape_vertices(shape)
        #points is a list of TopoDS_Vertex objects
        points = []
        for point in temp_points:
            points.append(make_point(point))
            print point
        #TODO: cluster points and make surfaces. but how do you compute the first parameter to build_plate?

if __name__ == "__main__":
    unittest.main()
    exit()
    from OCC.Display.wxSamplesGui import add_function_to_menu, add_menu, start_display
    add_menu("demo")
    add_function_to_menu("demo", demo)
    add_function_to_menu("demo", clear)
    add_function_to_menu("demo", ask_user)
    add_function_to_menu("demo", exit_app)
    init_display()
    start_display()

