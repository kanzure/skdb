from OCC.gp import *
from OCC.Precision import *
from OCC.BRepBuilderAPI import *
import OCC.Utils.DataExchange.STEP
from skdb import Connection, Part, Interface, Unit, FennObject, round
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
    raise NotImplementedError, "geom usable_point() only works with a list or a gp_Pnt"

def usable_vec(vector):
    '''returns a vector (or direction) even if you pass it a vector or gp_Vec or gp_Dir'''
    if type(vector) == type([]): return vector
    if type(vector) == gp_Vec or type(vector) == gp_Dir: return [vector.X(), vector.Y(), vector.Z()]
    raise NotImplementedError, "geom usable_vec() only works with a list or a gp_Vec or a gp_Dir"

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

def translation(point1=None, point2=None, vector=None):
    '''translate(point1, point2) -> gp_Trsf
    translate(vector) -> gp_Trsf'''
    new_trsf = gp_Trsf()
    if not point1==None and not point2==None: #two points
       point1 = safe_point(point1)
       point2 = safe_point(point2)
       vector = gp_Vec(point1, point2)
    elif not vector==None: #a vector
       vector = safe_vector(vector)
    new_trsf.SetTranslation(vector)
    return new_trsf

def rotation(rotation_pivot_point=None, direction=None, angle=None, gp_Ax1_given=None):
    '''rotation(rotation_pivot_point, direction, angle) -> gp_Trsf
    rotation(gp_Ax1, angle) -> gp_Trsf'''
    new_trsf = gp_Trsf()
    if not rotation_pivot_point==None and not direction==None and not angle==None:
       rotation_pivot_point = safe_point(rotation_pivot_point)
       direction = safe_dir(direction)
       ax1 = gp_Ax1(rotation_pivot_point, direction)
    elif not gp_Ax1_given==None and not angle==None:
       ax1 = gp_Ax1_given
    else: raise NotImplementedError, "rotation was given the wrong number of arguments."
    new_trsf.SetRotation(ax1, angle)
    return new_trsf

class OCC_triple(FennObject):
    doc_format = '''wraps %s: %s(1,2,3) or %s([1,2,3])
    Caution: assigning an attribute like "x" will not affect the underlying %s,
    you have to make a new one instead.'''
    def __init__(self, x=None, y=None, z=None, gp_pnt=None, gp_xyz=None):
        if not (x==None and y==None and z==None):
            if isinstance(x, list):
                self.x, self.y, self.z = float(x[0]), float(x[1]), float(x[2])
            else:
                self.x, self.y, self.z = float(x), float(y), float(z)
        elif not gp_pnt == None:
            self.x, self.y, self.z = gp_pnt.XYZ().X(), gp_pnt.XYZ().Y(), gp_pnt.XYZ().Z()
            self.post_init_hook()
            self = gp_pnt
            return
        elif not gp_xyz == None:
           self.x, self.y, self.z = gp_xyz.X(), gp_xyz.Y(), gp_xyz.Z()
           self.post_init_hook()
           self = gp_xyz
           return
        self.post_init_hook()
    def post_init_hook(self): 
        try: self.__class__.occ_class.__init__(self,self.x,self.y,self.z)
        except ValueError: self.__class__.occ_class.__init__(self) #return a null point
    def __eq__(self, other): 
        if not isinstance(other, self.__class__.occ_class): return False
        else: return self.IsEqual(other, Precision().Confusion()) == 1
    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.__class__.__name__, round(self.X()), round(self.Y()), round(self.Z()))
    def yaml_repr(self):
        return [round(self.X()), round(self.Y()), round(self.Z())]

class Point(OCC_triple, gp_Pnt):
    yaml_tag='!point'
    occ_class = gp_Pnt
    __doc__ = OCC_triple.doc_format % (occ_class, 'Point', 'Point', occ_class.__name__)
    def Transform(self, transform):
        result = gp_Pnt.Transformed(self, transform)
        return Point(gp_pnt=result)

class XYZ(OCC_triple, gp_XYZ):
    '''wraps gp_XYZ, mainly for the __repr__'''
    occ_class = gp_XYZ
    __doc__ = OCC_triple.doc_format % (occ_class, 'XYZ', 'XYZ', occ_class.__name__)
    #def __init__(self, gpxyz=None):
    #    gp_XYZ.__init__(self)
    #    if not gpxyz == None:
    #        self = gpxyz
    def __repr__(self):
        return "[%s, %s, %s]" % (self.X(), self.Y(), self.Z())

class Vector(OCC_triple, gp_Vec):
    yaml_tag='!vector'
    occ_class = gp_Vec
    __doc__ = OCC_triple.doc_format % (occ_class, 'Vector', 'Vector', occ_class.__name__)
    def __eq__(self, other):
        '''vec needs LinearTolerance and AngularTolerance'''
        if not isinstance(other, self.__class__.occ_class): return False
        else: return self.IsEqual(other, Precision().Confusion(), Precision().Confusion()) == 1

class Direction(OCC_triple, gp_Dir):
    yaml_tag='!direction'
    occ_class = gp_Dir
    __doc__ = OCC_triple.doc_format % (occ_class, 'Direction', 'Direction', occ_class.__name__)
    
class Transform(gp_Trsf):
    '''wraps gp_Trsf for stackable transforms'''
    def __init__(self, parent=None, description="root node"):
        gp_Trsf.__init__(self)
        self.children = []
        self.description = description
        if not parent==None:
            self.parent = parent
    def __repr__(self):
        '''see also Transform.get_children'''
        return self.description
    def process_result(self, trsf, description=""):
        '''hides some redundancy from the other methods'''
        new_transform = Transform(gptrsf=trsf, parent=self, description=description)
        self.children.append(new_transform)
        return new_transform
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
        '''multiplies all of the transforms together'''
        if self.children == []:
            return None
        if result == None:
            result = gp_Trsf()
        for each in self.children:
            result.Multiply(each.run())
        return result
    def Invert(self):
        '''wraps gp_Trsf.Inverted'''
        result = gp_Trsf.Inverted(self)
        return self.process_result(result, description="inverted")
    def Multiply(self, *args):
        '''wraps gp_Trsf.Multiplied'''
        result = gp_Trsf.Multiplied(self, args)
        return self.process_result(result, description="multiplied")
    def SetRotation(self, pivot_point=Point([0,0,0]), direction=Direction([0,0,1]), angle=Unit("pi/2 radians")):
        '''SetRotation(pivot_point=Point(), direction=Direction(), angle=Unit())'''
        new_transform = Rotation(parent=self, description="rotated", pivot_point=pivot_point, direction=direction, angle=angle)
        self.children.append(new_transform)
        return new_transform
    def SetTranslation(self, point1, point2):
        '''SetTranslation(point1=Point(), point2=Point())'''
        new_transform = Translation(parent=self, description="translated", point1=point1, point2=point2)
        self.children.append(new_transform)
        return new_transform
    def SetMirror(self, point):
        '''wraps gp_Trsf.Mirror -- mirror about a point'''
        self_copy = copy(self)
        result = gp_Trsf.SetMirror(self_copy, safe_point(point))
        desc = "mirrored about a point %s" % (usable_point(point))
        return self.process_result(result, description=desc)

class Rotation(Transform):
    '''a special type of Transform for rotation
    Rotation(pivot_point=Point(), direction=Direction(), angle=Unit())'''
    def __init__(self, pivot_point=Point([0,0,0]), direction=Direction([0,0,1]), angle=Unit("pi/2 radians"), parent=None, description=None):
        if not pivot_point and not direction and not angle: raise NotImplementedError, "you must pass parameters to Rotation.__init__"
        self.pivot_point = pivot_point
        self.direction = direction
        self.angle = angle
        Transform.__init__(self, parent=parent, description=description)
        gp_Trsf.SetRotation(self, gp_Ax1(pivot_point, direction), float(angle))
    def __repr__(self):
        '''just a guess for now, please test'''
        xyz = gp_Trsf.RotationPart(self)
        return "Rotation[%s, %s, %s]" % (xyz.X(), xyz.Y(), xyz.Z())

class Translation(Transform):
    '''a special type of Transform for translation
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
        Transform.__init__(self, parent=parent, description=description)
        gp_Trsf.SetTranslation(self, point1, point2)
    def __repr__(self):
        xyz = gp_Trsf.TranslationPart(self)
        return "Translation[%s, %s, %s]" % (xyz.X(), xyz.Y(), xyz.Z())

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
