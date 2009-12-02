from OCC.gp import *
from OCC.Precision import *
from OCC.BRepBuilderAPI import *
import OCC.Utils.DataExchange.STEP
from OCC.BRepPrimAPI import *
from OCC.TopoDS import *

#for BoundingBox
from OCC.Bnd import *
from OCC.BRepBndLib import *

#for exploring shapes
from OCC.BRep import BRep_Tool
from OCC.BRepTools import BRepTools_WireExplorer
from OCC.Utils.Topology import WireExplorer #wraps BRepTools_WireExplorer
from OCC.TopExp import TopExp_Explorer
from OCC.TopAbs import TopAbs_VERTEX, TopAbs_FACE, TopAbs_WIRE, TopAbs_EDGE

from skdb import Connection, Part, Interface, Unit, FennObject, prettyfloat
import os, math
from copy import copy, deepcopy
from string import Template

#where should this go?
def extend(first, second, overwrite=False):
    '''adds items in the second dictionary to the first
    overwrite=True means that the second dictionary is going to win in the case of conflicts'''
    third = first.copy()
    for second_key in second.keys():
        if first.get(second_key) is not None and overwrite:
            third[second_key] = copy(second[second_key])
        elif first.get(second_key) is None:
            third[second_key] = copy(second[second_key])
    return third

def move_shape(shape, from_pnt, to_pnt):
    trsf = gp_Trsf()
    trsf.SetTranslation(from_pnt, to_pnt)
    return BRepBuilderAPI_Transform(shape, trsf, True).Shape()
    
def point_shape(shape, direction):
    '''rotates a shape to point along origin's direction. this function ought to be unnecessary'''
    shape = BRepBuilderAPI_Transform(shape, point_along(Direction(direction)), True).Shape()
    return shape
    
def angle_to(x,y,z):                                                         
    '''returns polar coordinates in radians to a point from the origin            
    el rotates around the x-axis; then az rotates around the z axis; r is the distance'''
    azimuth = math.atan2(y, x) #longitude                                       
    elevation = math.atan2(z, math.sqrt(x**2 + y**2))                              
    radius = math.sqrt(x**2+y**2+z**2)                                                 
    return((azimuth-math.pi/2, elevation-math.pi/2, radius))  
    #glRotatef(az-90,0,0,1)                                                        
    #glRotatef(el-90,1,0,0) 

def point_along(direction):
    ox, oy, oz = 0, 0, 0
    dx, dy, dz = Direction(direction).Coord()
    (az, el, rad) = angle_to(dx-ox, dy-oy, dz-oz)
    #print "az: %s, el: %s, rad: %s... dx: %s, dy: %s, dz %s)" % (az, el, rad, dx, dy, dz)
    trsf = gp_Trsf()
    trsf.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(1,0,0)), el)
    trsf2 = gp_Trsf()
    trsf2.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), az)
    trsf2.Multiply(trsf)
    return trsf2
    
def build_trsf(point, x_vec, y_vec):
    point, x_vec, y_vec = Point(point), Direction(x_vec), Direction(y_vec)
    z_vec = Direction(x_vec.Crossed(y_vec))
    trsf=gp_Trsf()
    #from heekscad/src/Geom.cpp, sorta
    #TODO make sure x,y,z are orthonormal
    o, x, y, z = point.Coord(), x_vec.Coord(), y_vec.Coord(), z_vec.Coord()
    trsf.SetValues( x[0], y[0], z[0], o[0],
                            x[1], y[1], z[1], o[1],
                            x[2], y[2], z[2], o[2],
                            #0,     0,      0,     1,   #for you math types
                            0.0001, 0.00000001) #angular tolerance, linear tolerance
    return trsf

class OCC_triple(FennObject):
    '''simplifies wrapping pythonOCC classes like gp_Pnt, gp_Vec etc'''
    doc_format = Template('''wraps $occ_class: $cls(1,2,3) or $cls([1,2,3]) or $cls($occ_name(1,2,3))
    Caution: assigning an attribute like "x" will not affect the underlying $occ_name,
    you have to make a new one instead.''')
    wrapped_classes = gp_Pnt, gp_Vec, gp_Dir, gp_XYZ
    def __init__(self, x=None, y=None, z=None):
        if isinstance(x, self.__class__): #Point(Point(1,2,3))
            self.__dict__ = copy(x.__dict__) #does this use the same gp_Pnt object? (it shouldnt)
        for cls in OCC_triple.wrapped_classes: 
            if isinstance(x, cls): #Point(gp_Pnt()) or Point(Vector(1,2,3))
                self.x, self.y, self.z = (x.X(), x.Y(), x.Z())
                self.post_init_hook(); return
        if isinstance(x, list) or isinstance(x, tuple):
            self.x, self.y, self.z = float(x[0]), float(x[1]), float(x[2])
        elif x is not None and y is not None and z is not None:
            self.x, self.y, self.z = float(x), float(y), float(z)
        self.post_init_hook()
    def post_init_hook(self): #for instantiating from yaml
        try: self.__class__.occ_class.__init__(self,self.x,self.y,self.z)
        except AttributeError: self.__class__.occ_class.__init__(self) #return a null point
    def __eq__(self, other): 
        if not isinstance(other, self.__class__.occ_class): return False
        else: return (self.IsEqual(other, Precision().Confusion()) == 1)
    def __cmp__(self, other):
        if other.x==self.x and other.y==self.y and other.z==self.z: return 0
        elif other.x>self.x and other.y>self.y and other.z>self.z: return -1
        elif self.x>other.x and self.y>other.y and self.z>other.z: return 1
        else: return None #not really meaningful
    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__, prettyfloat(self.X()), prettyfloat(self.Y()), prettyfloat(self.Z()))
    def yaml_repr(self):
        return [prettyfloat(self.X()), prettyfloat(self.Y()), prettyfloat(self.Z())]
    def transformed(self, transformation):
        '''transform is a verb'''
        return self.__class__(self.occ_class.Transformed(self, transformation))
    def reversed(self):
        return self.__class__(self.occ_class.Reversed(self))

#TODO: Point from a TopoDS_Vertex please
#Point(TopoDS_Vertex()) -> Point(BRep_Tool().Pnt(TopoDS_Vertex())) but only if the vertex.Location().IsDifferent(TopLoc_Location())==1
class Point(OCC_triple, gp_Pnt):
    yaml_tag='!point'
    occ_class = gp_Pnt
    #other_occ_class = OCC.BRep.BRep_Tool.Pnt(TopoDS_Vertex) -> gp_Pnt
    __doc__ = OCC_triple.doc_format.safe_substitute(occ_class=occ_class, cls='Point', occ_name = occ_class.__name__)

class XYZ(OCC_triple, gp_XYZ):
    occ_class = gp_XYZ
    __doc__ = OCC_triple.doc_format.safe_substitute(occ_class=occ_class, cls='XYZ', occ_name = occ_class.__name__)
    def __repr__(self):
        return "[%s, %s, %s]" % (self.X(), self.Y(), self.Z())

class Vector(OCC_triple, gp_Vec):
    yaml_tag='!vector'
    occ_class = gp_Vec
    __doc__ = OCC_triple.doc_format.safe_substitute(occ_class=occ_class, cls='Vector', occ_name = occ_class.__name__)
    def __eq__(self, other):
        '''vec needs LinearTolerance and AngularTolerance'''
        if not isinstance(other, self.__class__.occ_class): return False
        else: return self.IsEqual(other, Precision().Confusion(), Precision().Confusion()) == 1

class Direction(OCC_triple, gp_Dir):
    yaml_tag='!direction'
    occ_class = gp_Dir
    __doc__ = OCC_triple.doc_format.safe_substitute(occ_class=occ_class, cls='Vector', occ_name = occ_class.__name__)

class Transformation(gp_Trsf):
    '''wraps gp_Trsf for stackable transformations'''
    def __init__(self, parent=None, description="root node"):
        gp_Trsf.__init__(self)
        self.children = []
        self.description = description
        if parent:
            self.parent = parent
    def __repr__(self):
        '''see also Transformation.get_children'''
        return self.description
    def process_result(self, trsf, description=""):
        '''hides some redundancy from the other methods'''
        new_transformation = Transformation(gptrsf=trsf, parent=self, description=description)
        self.children.append(new_transformation)
        return new_transformation
    def get_children(self):
        '''returns a list of all children'''
        if self.children == []:
            return None
        return_list = copy(self.children)
        for each in self.children:
            more = each.get_children()
            if more:
                return_list.append(more)
        return return_list
    def run(self, result=None):
        '''multiplies all of the Transformations together'''
        if self.children == []:
            return self
        if result == None:
            result = Transformation()
        for each in self.children:
            result.Multiply(each.run())
        return result
    def Invert(self):
        '''wraps gp_Trsf.Inverted'''
        result = gp_Trsf.Inverted(self)
        return self.process_result(result, description="inverted")
    def Multiplied(self, *args):
        '''wraps gp_Trsf.Multiplied'''
        result = gp_Trsf.Multiplied(self, args)
        return self.process_result(result, description="multiplied")
    def SetRotation(self, pivot_point=Point([0,0,0]), direction=Direction([0,0,1]), angle=Unit("pi/2 radians")):
        '''SetRotation(pivot_point=Point(), direction=Direction(), angle=Unit())'''
        new_transformation = Rotation(parent=self, description="rotated", pivot_point=pivot_point, direction=direction, angle=angle)
        self.children.append(new_transformation)
        return new_transformation
    def SetTranslation(self, point1, point2):
        '''SetTranslation(point1=Point(), point2=Point())'''
        new_transformation = Translation(parent=self, description="translated", point1=point1, point2=point2)
        self.children.append(new_transformation)
        return new_transformation
    def SetMirror(self, point):
        '''wraps gp_Trsf.Mirror -- mirror about a point'''
        self_copy = copy(self)
        result = gp_Trsf.SetMirror(self_copy, Point(point))
        desc = "mirrored about %s" % (point)
        return self.process_result(result, description=desc)

class Rotation(Transformation):
    '''a special type of Transformation for rotation
    Rotation(pivot_point=Point(), direction=Direction(), angle=Unit())'''
    def __init__(self, pivot_point=Point([0,0,0]), direction=Direction([0,0,1]), angle=Unit("pi/2 radians"), parent=None, description=None):
        if not pivot_point and not direction and not angle: raise NotImplementedError, "you must pass parameters to Rotation.__init__"
        self.pivot_point = pivot_point
        self.direction = direction
        self.angle = angle
        Transformation.__init__(self, parent=parent, description=description)
        gp_Trsf.SetRotation(self, gp_Ax1(pivot_point, direction), float(angle))
    def __repr__(self):
        '''just a guess for now, please test'''
        xyz = gp_Trsf.RotationPart(self)
        return "Rotation[%s, %s, %s]" % (xyz.X(), xyz.Y(), xyz.Z())

class Translation(Transformation):
    '''a special type of Transformation for translation
    Translation(point1=, point2=)
    Translation(vector=) (not implemented)'''
    def __init__(self, point1=None, point2=None, vector=None, parent=None, description=None):
        if not point1 and not point2 and not vector: raise NotImplementedError, "you must pass parameters to Translation.__init__"
        if vector: raise NotImplementedError, "Translation.__init__ doesn't yet take a vector (sorry)" #FIXME
        self.point1 = point1
        self.point2 = point2
        self.vector = vector
        self.parent = parent
        self.description = description
        self.children = []
        Transformation.__init__(self, parent=parent, description=description)
        gp_Trsf.SetTranslation(self, point1, point2)
    def __repr__(self):
        xyz = gp_Trsf.TranslationPart(self)
        return "Translation[%s, %s, %s]" % (xyz.X(), xyz.Y(), xyz.Z())

def mate_connection(connection): 
    '''returns the gp_Trsf to move/rotate i2 to connect with i1. should have no side effects'''
    import math
    i1, i2 = connection.interface1, connection.interface2
    if i1.part.transformation is None: i1.part.transformation = gp_Trsf()
    opposite = gp_Trsf()
    opposite.SetRotation(gp_Ax1(Point(i1.point), Direction(i1.x_vec)), math.pi) #rotate 180 so that interface z axes are opposed
    t = gp_Trsf()
    t.Multiply(i1.part.transformation)
    t.Multiply(opposite)
    t.Multiply(i1.get_transformation())
    t.Multiply(i2.get_transformation().Inverted())
    return t

class GayError(Exception): pass

def naive_coincidence_fixer(parts, cgraph=None):
    '''connects compatible interfaces that happen to be in the same place; think lego.
    this is slow because it compares every interface to every other interface.'''
    all_i = set()
    for brick in parts:
        for i in brick.interfaces:
            all_i.add(i)
    for i in all_i:
        for j in all_i:
            if i is j: break
            ipt = Point(i.point).transformed(i.part.transformation)
            jpt = Point(j.point).transformed(j.part.transformation)
            if ipt.IsEqual(jpt, 1): #within 1 mm
                if i.get_z_vec().transformed(i.part.transformation).IsEqual( j.get_z_vec().transformed(i.part.transformation).reversed(), 1, 0.01): #within 1mm and some angle
                    #interfaces lined up
                    if i.compatible(j):
                        if i.connected and j.connected: break
                        Connection(i, j).connect(cgraph=cgraph)
                        i.show(color='GREEN'); j.show(color='RED')
                    else: raise GayError, "your nubs are touching"
   
#skdb.Interface
def get_transformation(self): #i wish this were a property instead
    '''returns the transformation to align the interface vector at the origin along the Z axis'''
    trsf = gp_Trsf()
    z_vec = self.get_z_vec #find the interface vector
    return build_trsf(self.point, self.x_vec, self.y_vec)
Interface.get_transformation = get_transformation

def get_z_vec(self):
    '''return the interface mating vector relative to the part'''
    return Vector(Vector(self.x_vec).Crossed(Vector(self.y_vec)))
Interface.get_z_vec = get_z_vec

#skdb.Part
def load_CAD(self):
    '''load this object's CAD file. assumes STEP.'''
    if not hasattr(self, "package"): return
    #assert hasattr(self,"package"), "Part.load_CAD doesn't have its package loaded (load_package)."
    #FIXME: assuming step
    for file in self.files:
        full_path = os.path.join(self.package.path(), str(file))
        #TODO: silence STEPImporter
        my_step_importer = OCC.Utils.DataExchange.STEP.STEPImporter(full_path)
        my_step_importer.ReadFile()
        self.shapes = my_step_importer.GetShapes()
        for i in range(len(self.shapes)):
            self.shapes[i] = self.shapes[i]
        self.compound = my_step_importer.GetCompound()
        #set the bounding box
        self._bounding_box = BoundingBox(self.shapes[0])
    return
Part.load_CAD = load_CAD

def make_face(shape):
    face = BRepBuilderAPI_MakeFace(shape)
    face.Build()
    return Face(face.Face())

def make_edge2d(shape):
    spline = BRepBuilderAPI_MakeEdge2d(shape)
    spline.Build()
    return Edge(spline.Edge())

def make_edge(shape):
    spline = BRepBuilderAPI_MakeEdge(shape)
    spline.Build()
    return Edge(spline.Edge())

class OCC_shape(TopoDS_Shape):
    occ_class = TopoDS_Shape #just a default
    def __init__(self, incoming=None):
        if isinstance(incoming, self.__class__): #Face(Face()), Shape(Shape()), etc.
            #if self.occ_class is not TopoDS_Shape:
            TopoDS_Shape.__init__(self)
            self.occ_class.__init__(self) #yes, no? dunno
            self.__dict__ = extend(self.__dict__, incoming.__dict__, overwrite=False)
            self.TShape(incoming.TShape())
        elif isinstance(incoming, self.occ_class):
            #if self.occ_class is not TopoDS_Shape:
            TopoDS_Shape.__init__(self)
            self.occ_class.__init__(self)
            self.__dict__ = extend(self.__dict__, incoming.__dict__, overwrite=False)
            other_shape = incoming.TShape()
            self.TShape(other_shape)
        elif isinstance(incoming, TopoDS_Shape):
            TopoDS_Shape.__init__(self)
            self.occ_class.__init__(self)
            self.__dict__ = extend(self.__dict__, incoming.__dict__, overwrite=False)
            other_shape = incoming.TShape()
            self.TShape(other_shape)
    def __copy__(self):
        '''copies only the shape and returns a Shape with the shape'''
        #note that occ uses TopoDS_Shape().TShape() for some reason.
        current_shape = copy(self.TShape())
        new_shape = Shape()
        new_shape.TShape(current_shape)
        return new_shape
    def get_wires(self):
        '''traverses a face (or a shape) for wires
        you might want get_edges instead?
        returns a list of wires'''
        wires = []
        #if isinstance(self, Shape): to_explore = self
        #else: to_explore = Shape(self)
        to_explore = self
        explorer = TopExp_Explorer(to_explore, TopAbs_WIRE, TopAbs_EDGE)
        explorer.ReInit()
        while explorer.More():
            #edge = TopoDS().Edge(explorer.Current())
            #wire = BRepBuilderAPI_MakeWire(edge).Wire()
            wire = TopoDS().Wire(explorer.Current())
            wire1 = Wire(wire)
            wires.append(wire1)
            explorer.Next()
        return wires
    def get_edges(self):
        '''sometimes what you really want is get_edges instead of get_wires. (a wire will not have points, but an edge will)
        can someone make sense of this please?'''
        edges = []
        explorer = TopExp_Explorer(self, TopAbs_EDGE)
        explorer.ReInit()
        while explorer.More():
            edge = TopoDS().Edge(explorer.Current())
            edge1 = Edge(edge)
            edges.append(edge1)
            explorer.Next()
        return edges
    def get_faces(self):
        '''returns a list of faces for the given shape
        note that it could be that the entire shape is really just a face, so don't be upset if this returns []'''
        faces = []
        explorer = TopExp_Explorer(self, TopAbs_FACE)
        while explorer.More():
            face = Face(TopoDS().Face(explorer.Current()))
            faces.append(face)
            explorer.Next()
        return faces
    def get_points(self, edges=True, wires=True):
        '''returns a list of points defining the shape
        based off of wires and faces'''
        points = []
        #wires = self.wires
        faces = self.faces
        #for wire in wires:
        #    print "get_points: processing a wire"
        #    points.extend(wire.points)
        for face in faces:
            points.extend(face.get_points(edges=edges,wires=wires))
        points = list(set(points)) #filter out the repeats
        return points
    def get_shape(self):
        '''returns the TShape object
        occ only, this probably isn't useful anywhere else'''
        return self.TShape()
    def set_shape(self, value):
        '''sets the TShape'''
        if isinstance(value, Handle_TopoDS_TShape):
            self.TShape(value)
        elif isinstance(value, self.__class__):
            self.TShape(value.TShape())
        elif isinstance(value, self.occ_class):
            self.TShape(value.TShape())
        elif isinstance(value, self.occ_class_handler):
            #set_shape(Handle_TopoDS_TFace)
            self.TShape(value.GetObject().TShape())
        else: raise ValueError, "OCC_shape.set_shape: not sure what to do, possibilities exhausted for %s" % (value)
    wires = property(fset=None, fget=get_wires, doc="a list of wires (partially) defining the shape")
    edges = property(fset=None, fget=get_edges, doc="a list of edges (partially) defining the shape")
    faces = property(fset=None, fget=get_faces, doc="a list of faces (partially) defining the shape")
    points = property(fset=None, fget=get_points, doc="a list of points (partially) defining the shape")
    shape = property(fset=set_shape, fget=get_shape, doc="wraps occ TopoDS_Shape TShape")

class Wire(OCC_shape, TopoDS_Wire):
    occ_class = TopoDS_Wire
    occ_class_handler = Handle_TopoDS_TWire
    def get_points(self):
        '''takes a wire and extracts points
        returns a list of points'''
        vertices = []
        #the short version:
        #vertices.extend(WireExplorer(self).ordered_vertices())
        #return vertices
        my_wire = self
        #my_wire = TopoDS().Wire(self)
        #my_wire = TopoDS().Wire(Shape(self.shape))
        #my_wire = Wire(self)
        #explorer = BRepTools_WireExplorer(self)
        explorer = TopExp_Explorer(self, TopAbs_VERTEX)
        while explorer.More():
            vertex = TopoDS().Vertex(explorer.Current())
            xyz = Point(BRep_Tool().Pnt(vertex))
            #if not xyz == Point():
            vertices.append(xyz)
            explorer.Next()
        return vertices    
    points = property(fget=get_points, fset=None, doc="a list of points defining this wire")
    faces = None
    wires = None

class Edge(OCC_shape, TopoDS_Edge):
    occ_class = TopoDS_Edge
    occ_class_handler = Handle_TopoDS_TEdge
    def get_points(self):
        '''returns a list of points making up this edge'''
        points = []
        explorer = TopExp_Explorer(self, TopAbs_VERTEX)
        while explorer.More():
            vertex = TopoDS().Vertex(explorer.Current())
            point = Point(BRep_Tool().Pnt(vertex))
            #one day: point = Point(vertex) where vertex is of type TopoDS_Vertex
            #if not point == Point():
            points.append(point)
            explorer.Next()
        return points
    points = property(fget=get_points, fset=None, doc="a list of points defining this edge")
    faces = None
    wires = None

class Face(OCC_shape, TopoDS_Face):
    occ_class = TopoDS_Face
    occ_class_handler = Handle_TopoDS_TFace
    def get_points(self, edges=True, wires=True):
        points = []
        wirelist = self.wires #get_wires()
        edgelist = self.edges #get_edges()
        wire_pts = []
        edge_pts = []
        if wires == True:
            for wire in wirelist:
                wire_pts.extend(wire.points)
        if edges == True:
            for edge in edgelist:
                edge_pts.extend(edge.points)
        #if len(wire_pts) == 0: points.extend(edge_pts)
        #elif len(edge_pts) == 0: points.extend(wire_pts)
        #else: points.extend(wire_pts) #just choose one
        points.extend(edge_pts)
        points.extend(wire_pts)
        return points
    points = property(fget=get_points, fset=None, doc="a list of points defining this wire")
    faces = None

#can we call this something else please?
class Shape(OCC_shape):
    occ_class = TopoDS_Shape
    occ_class_handler = Handle_TopoDS_TShape
    def __repr__(self):
        return "some shape"
    def yaml_repr(self):
        return "unyamlifiable"
    def __eq__(self, other): #woah wtf
        return True
        if not isinstance(other, TopoDS_Shape): return False
        else: return True #self.IsEqual(other)

class BoundingBox:
    '''finds the extents of an object along each axis. useful for checking against sorted coordinates.
    implements axis-aligned bounding box: http://www.gamedev.net/dict/term.asp?TermID=309
    use this after applying rotations and translations to your shape
    '''
    def __init__(self, shape=None, point1=None, point2=None):
        '''please either provide only shape or provide only minimums and maximums
        if given both, the values are recomputed'''
        if shape is not None:
            assert isinstance(shape, TopoDS_Shape)
            #compute the box from the shape
            self.box = Bnd_Box()
            BRepBndLib().Add(shape, self.box)
            self.x_min, self.y_min, self.z_min, self.x_max, self.y_max, self.z_max = self.box.Get()
            self.point1, self.point2 = self._determine_points()
        else: 
            x1, y1, z1 = point1.Coord()
            x2, y2, z2 = point2.Coord()
            self.x_min, self.x_max = min(x1, x2), max(x1, x2)
            self.y_min, self.y_max = min(y1, y2), max(y1, y2)
            self.z_min, self.z_max = min(z1, z2), max(z1, z2)
            
    def _determine_points(self):
        point1 = Point(self.x_min, self.y_min, self.z_min)
        point2 = Point(self.x_max, self.y_max, self.z_max)
        return [point1, point2]
        
    def make_box(self):
        '''returns a Shape representing this bounding box. maybe useful for visualization?'''
        self._determine_points()
        return Shape(BRepPrimAPI_MakeBox(self.point1, self.point2).Shape())
        
    def interferes(self, other): 
        '''if one object's left or right bound lies between the other object's left and right bounds,
        then the two objects have overlapping X ranges.
        if two objects overlap along all three axes, they have collided.'''
        #this relies on point1 and point2 being used properly, which i don't particularly like
        if self.point1.X() > other.point2.X(): return False
        if self.point1.Y() > other.point2.Y(): return False
        if self.point1.Z() > other.point2.Z(): return False
        if self.point2.X() < other.point1.X(): return False
        if self.point2.Y() < other.point1.Y(): return False
        if self.point2.Z() < other.point1.Z(): return False
        return True
        
    def contains(self, other):
        '''uses OCC Bnd_Box method'''
        if self.box.IsOut(other): return false
        else: return True

    def __deepcopy__(self, memo):
        return self.__class__(point1=Point(self.x_min, self.y_min, self.z_min), point2=Point(self.x_max, self.y_max, self.z_max))
    def __repr__(self):
        return "BoundingBox(x=[%s, %s], y=[%s, %s], z=[%s, %s])" % (self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max)

def shape_extractor(part):
    '''breaks up a shape into a number of separate shapes
    ultimately the plan is to let users click on individual interfaces in the gui
    returns a list of shapes'''
    raise NotImplementedError, "bryan hasnt got to this yet"
    shape = part.shape #or part.shapes[0]
    faces = shape.get_faces()
    for face in faces:
        #points = face.get_points()
        #turn this face into a shape
        new_shape = Shape(face)
    #draw all the faces, wires, and points to make the same overall OCC_shape ?

def shape_nearest(point, shapes):
    '''returns which shape out of the list is closest to the specified point
    ideally this can help figure out which surface is closest to an Interface point on a part'''
    pass

