from OCC.gp import *
from OCC.BRepBuilderAPI import *
import OCC.Utils.DataExchange.STEP
from skdb import Connection, Part, Interface, Unit
import os, math
from copy import copy, deepcopy

def safe_point(point):
    '''returns a gp_Pnt, even if you give it a gp_Pnt'''
    if type(point) == gp_Pnt: return point
    return gp_Pnt(point[0],point[1],point[2])

def safe_vec(vector):
    '''returns a gp_Vec, even if you give it a gp_Vec'''
    if type(vector) == gp_Vec: return vector
    return gp_Vec(vector[0], vector[1], vector[2])

def safe_dir(direction):
    '''returns a gp_Dir, even if you give it a gp_Dir'''
    if type(direction) == gp_Dir: return direction
    return gp_Dir(direction[0], direction[1], direction[2])

def usable_point(point):
    '''returns a point even if you pass it a point or gp_Pnt'''
    if type(point) == type([]): return point
    if type(point) == gp_Pnt: return [point.XYZ().X(), point.XYZ().Y(), point.XYZ().Z()]
    assert NotImplementedError, "geom usable_point() only works with a list or a gp_Pnt"

def usable_vec(vector):
    '''returns a vector (or direction) even if you pass it a vector or gp_Vec or gp_Dir'''
    if type(vector) == type([]): return vector
    if type(vector) == gp_Vec or type(vector) == gp_Dir: return [vector.X(), vector.Y(), vector.Z()]
    assert NotImplementedError, "geom usable_vec() only works with a list or a gp_Vec or a gp_Dir"

def usable_dir(direction):
    '''returns a direction even if you pass it a direction or gp_Dir'''
    return usable_vec(direction)

def move_shape(shape, from_pnt, to_pnt, trsf_only=True):
    trsf = gp_Trsf()
    trsf.SetTranslation(from_pnt, to_pnt)
    if trsf_only: return trsf
    else: return BRepBuilderAPI_Transform(shape, trsf, True).Shape()

def angle_to(x,y,z):                                                         
    '''returns polar coordinates in radians to a point from the origin            
    a rotates around the x-axis; b rotates around the y axis; r is the distance'''
    azimuth = math.atan2(y, x) #longitude                                       
    elevation = math.atan2(z, math.sqrt(x**2 + y**2))                              
    radius = math.sqrt(x**2+y**2+z**2)                                                 
    return((azimuth, elevation, radius))  
    #glRotatef(az-90,0,0,1)                                                        
    #glRotatef(el-90,1,0,0) 

def point_shape(shape, origin, trsf_only=False):
    '''rotates a shape to point along origin's direction. this function ought to be unnecessary'''
    assert type(origin) == gp_Ax1
    #ox, oy, oz = origin.Location().X(), origin.Location().Y(), origin.Location().Z() #ffs
    ox, oy, oz = 0, 0, 0
    dx, dy, dz = origin.Direction().X(), origin.Direction().Y(), origin.Direction().Z()
    (az, el, rad) = angle_to(dx-ox, dy-oy, dz-oz)
    #print "az: %s, el: %s, rad: %s... dx: %s, dy: %s, dz %s)" % (az, el, rad, dx, dy, dz)
    trsf = gp_Trsf()
    trsf.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(1,0,0)), el-math.pi/2)
    trsf2 = gp_Trsf()
    trsf2.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), az-math.pi/2)
    trsf.Multiply(trsf2)
    if trsf_only: 
        return trsf
    else:
        shape = BRepBuilderAPI_Transform(shape1, trsf, True).Shape()
        return shape

class Transform:
    '''used for keeping track of the translation and rotation of a part
    Part.transforms = [] #should be a list of Transform objects
    all methods should have no side effects (except modifying local attributes)'''
    gp_Trsf_object = None
    descriptions = [] #list of descriptions; you will be a user's best friend if you maintain this list.
    def __init__(self, gp_Trsf_obj, description=None):
        self.set_transform(gp_Trsf_inst=gp_Trsf_obj)
        if not description == None:
            self.descriptions.append(description)
    def __repr__(self):
        '''spits out a human-readable representation of what this Transform actually does'''
        return str(self.descriptions)
    def set_transform(self, gp_Trsf_inst=None, brepbuilderapi_transform_inst=None):
        '''maybe you want to reset one of the transforms for this Transform; other wrapper stuff goes on here.'''
        if not gp_Trsf_inst == None and not brepbuilderapi_transform_inst == None: assert "Transform.set_transform() can only set one transform at a time."
        if not gp_Trsf_inst == None:
            self.gp_Trsf_object = gp_Trsf_inst
            self.update_brepbuilderapi_transform()
        if not brepbuilderapi_transform_inst == None:
            self.brepbuilderapi_transform_object = brepbuilderapi_transform_inst
            self.update_gp_trsf()
    def update_brepbuilderapi_transform(self):
        '''an internal method. updates brepbuilderapi_transform_object based off of the current status of gp_Trsf_obj'''
        self.brepbuilderapi_transform_object = BRepBuilderAPI_Transform(self.gp_Trsf_object)
    #not sure about this next one
    def update_gp_trsf(self):
        '''an internal method. updates gp_Trsf_object based off of the current status of brepbuilderapi_transform_object'''
        assert NotImplementedError, "Transform.set_gp_trsf(): Not sure if you're able to get a gp_Trsf from a BRepBuilderAPI_Transform"
    def point_in_dir(self, point1=[0,0,0], direction1=[0,0,1]):
        '''modifies the Transform so that it will make a shape point in a direction.
        based off of point_shape'''
        point1 = safe_point(point1)
        direction1 = safe_dir(direction1)
        ox, oy, oz = 0, 0, 0
        dx, dy, dz = direction1.Direction().X(), direction1.Direction().Y(), direction1.Direction().Z()
        (az, el, rad) = angle_to(dx-ox, dy-oy, dz-oz)
        trsf = gp_Trsf()
        trsf.SetRotation(gp_Ax1(point1, gp_Dir(1,0,0)), el-math.pi/2)
        trsf2 = gp_Trsf()
        trsf2.SetRotation(gp_Ax1(point1, gp_Dir(0,0,1)), az-math.pi/2)
        trsf.Multiply(trsf2) #why?
        self.gp_Trsf_object.Multiply(trsf) #just a guess 
    def perform_shape(self, shape):
        '''returns an ais_shape. input shape should be a TopoDS_Shape. applies the transform.'''
        self.set_brepbuilderapi_transform()
        resulting_shape = copy(shape) #should that be deepcopy?
        self.brepbuilderapi_transform.Perform(resulting_shape)
        return resulting_shape.Shape()
    def perform_point(self, point1):
        '''perform this transform on a point, returns a new gp_Pnt'''
        point1 = safe_point(point1)
        return point1.Transformed(self.gp_Trsf_object)
    def describe(self, description):
        '''if you call this every time you update the transformation, you will be a user's best friend (also, __repr__ will work)
        note that SetTranslation and SetRotation automatically call this
        think of it as a logging utility or toy'''
        self.descriptions.append(description)
    #wrap up some gp_Trsf methods
    def SetTranslation(self, *args):
        '''SetTranslation(point1, point2)
        SetTranslation(vector)'''
        if len(args) == 2: #two points
            point1 = safe_point(args[0])
            point2 = safe_point(args[1])
            vector = gp_Vec(point1, point2)
            self.describe("translate from %s to %s" % (usable_point(point1), usable_point(point2)))
        elif len(args) == 1: #a vector
            vector = safe_vector(args[0])
            self.describe("translate with vector %s" % (usable_vec(vector)))
        self.gp_Trsf_object.SetTranslation(vector)
        self.update_brepbuilderapi_transform()
    def SetRotation(self, *args):
        '''SetRotation(rotation_pivot_point, direction, angle)
        SetRotation(gp_Ax1, angle)'''
        if len(args) == 3:
            rotation_pivot_point = safe_point(args[0])
            direction = safe_dir(args[1])
            angle = args[2]
            ax1 = gp_Ax1(rotation_pivot_point, direction)
            self.describe("rotate an angle of %s radians in the %s direction" % (angle, usable_dir(direction)))
        elif len(args) == 2:
            ax1 = args[0]
            angle = args[1]
            self.describe("rotate an angle of %s radians in some undecipherable direction" % (angle))
        else: assert NotImplementedError, "Transform.SetRotation was given the wrong number of arguments."
        self.gp_Trsf_object.SetRotation(ax1, angle)
        self.update_brepbuilderapi_transform()

class Mate(Connection):
    def transform(self): 
        '''returns the gp_Trsf to move/rotate i2 to connect with i1. should have no side effects'''
        i1, i2 = self.interface1, self.interface2
        #this is lame
        i1.x_vec = safe_vec(i1.x_vec)
        i1.y_vec = safe_vec(i1.y_vec)
        i2.x_vec = safe_vec(i2.x_vec)
        i2.y_vec = safe_vec(i2.y_vec)
        i1.point = safe_point(i1.point)
        i2.point = safe_point(i2.point)
        i1.z_vec = copy(i1.x_vec); i1.z_vec.Cross(i1.y_vec)
        orient_i1 = point_shape(i1.part.shapes[0], gp_Ax1(gp_Pnt(0,0,0), gp_Dir(i1.z_vec)), trsf_only=True)
        #move_i1 = gp_Trsf() #don't move the first part
        #trsf_i1 = move_i1.Multiplied(orient_i1)
        trsf_i1 = orient_i1
        if hasattr(i1.part, "transform"):
            tmp = i1.point.Transformed(i1.part.transform)
        else: tmp = i1.point
        #tmp = i1.point.Transformed(trsf_i1)
        i2.z_vec = copy(i2.x_vec); i2.z_vec.Cross(i2.y_vec)
        orient_i2 = point_shape(i2.part.shapes[0], gp_Ax1(gp_Pnt(0,0,0), gp_Dir(i2.z_vec)), trsf_only=True)
        opposite = gp_Trsf()
        opposite.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(gp_Vec(1,0,0))), math.pi) #rotate 180 so that interface z axes are opposed
        move_i2 =  move_shape(i2.part.shapes[0], tmp, i2.point, trsf_only=True)
        trsf_i2 = move_i2.Multiplied(orient_i2)
        trsf_i2 = trsf_i2.Multiplied(opposite)
        #if hasattr(i2.part, "transform"):
        #    trsf_i2 = trsf_i2.Multiplied(i2.part.transform)
        print "x: %.1f y: %.1f z: %.1f" % trsf_i2.TranslationPart().Coord()
        return trsf_i2
        
    def apply(self):
        '''i dont think this modifies i2.part'''
        print "connecting %s to %s" % (self.interface1.name, self.interface2.name)
        self.interface2.part.transform = self.transform()
        return [BRepBuilderAPI_Transform(shape, self.transform(), True).Shape() for shape in self.interface2.part.shapes]
    
#skdb.Part
def load_CAD(self):
    '''load this object's CAD file. assumes STEP.'''
    if len(self.files) == 0: return #no files to load
    assert hasattr(self,"package"), "Part.load_CAD doesn't have its package loaded."
    #FIXME: assuming STEP
    #TODO: check/verify filename path
    #FIXME: does not properly load in models from multiple files (2009-07-30)
    for file in self.files:
        full_path = os.path.join(self.package.path(), str(file))
        my_step_importer = OCC.Utils.DataExchange.STEP.STEPImporter(full_path)
        my_step_importer.ReadFile()
        self.shapes = my_step_importer.GetShapes()
        self.compound = my_step_importer.GetCompound()
    #i, j, k, point = self.interfaces[0].i, self.interfaces[0].j, self.interfaces[0].k, self.interfaces[0].point
    #x,y,point = self.interfaces[0].x,self.interfaces[0].y,self.interfaces[0].point
    return self.shapes

Part.load_CAD = load_CAD
def add_shape(self, result):
    '''add a shape to self.ais_shapes. this isn't as exciting as you think it is.'''
    if type(result) == type([]): self.ais_shapes = result[0]
    else: self.ais_shapes = result
    return
Part.add_shape = add_shape

def get_point(self): return list(self.__gp_Pnt_point.Coord())
def set_point(self, value): 
    if isinstance(value, Unit):
        raise NotImplementedError, 'coords must be in mm'
    self.__gp_Pnt_point = gp_Pnt(val[0], val[1], val[2])
def del_point(self): del self.__gp_Pnt_point

def get_gp_Pnt(self):
    return self.__gp_Pnt

def transformed(self, trsf):
    return self.__gp_Pnt.Transformed(trsf)

#stuff the class with new funcs
for i in [load_CAD, add_shape, get_gp_Pnt, transformed]:
    setattr(Part, i.__name__, i)

#for some reason property doesn't accept properties or have a __name__. so much for OO
Part.point = property(get_point, set_point, del_point)
