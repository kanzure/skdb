from OCC.gp import *
from OCC.BRepBuilderAPI import *
from skdb import Connection, Part, Interface
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


class Mate(Connection):
    def transform(self): 
        '''returns the gp_Trsf to move/rotate i2 in place on i1. should have no side effects'''
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
        move_i1 = gp_Trsf() #don't move the first part
        trsf_i1 = orient_i1.Multiplied(move_i1)
        tmp = i1.point.Transformed(trsf_i1)
        i2.z_vec = copy(i2.x_vec); i2.z_vec.Cross(i2.y_vec)
        orient_i2 = point_shape(i2.part.shapes[0], gp_Ax1(gp_Pnt(0,0,0), gp_Dir(i2.z_vec)), trsf_only=True)
        move_i2 =  move_shape(i2.part.shapes[0], tmp, i2.point, trsf_only=True)
        trsf_i2 = orient_i2.Multiplied(move_i2)
        return trsf_i2
        
    def apply(self):
        '''i dont think this modifies i2.part'''
        print "connecting %s to %s" % (self.interface1.name, self.interface2.name)
        return BRepBuilderAPI_Transform(self.interface2.part.shapes[0], self.transform(), True).Shape()
    
try:
        import OCC.Utils.DataExchange.STEP
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

except ImportError: print "Couldn't import OCC.Utils.DataExchange.STEP: Is pythonOCC installed properly?"