#!/usr/bin/python
#defines pymates.interface.Interface
import yaml
import math

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag = '!interface'
    def __init__(self, name="generic interface name", units=None, geometry=None, point=[0,0,0], x=0, y=0, z=0, hermaphroditic=False, part=None):
        '''rotate first about x, then about z. give x and z in degrees (__init__ autoconverts to radians)'''
        self.name, self.units, self.geometry, self.degrees, self.hermaphroditic, self.part = name, units, geometry, False, hermaphroditic, part
        self.point, self.x, self.y, self.z = point, x, y, z
        self.mated = None
        self.identifier = None
    def compatible(self, other):
        '''really really generic: it's compatible if it's the first one'''
        if not other.mated:
            return True
        else: return False
    def convert(self):
        '''convert from degrees to radians for rotational information'''
        if not hasattr(self, "degrees"):
            self.degrees = True
        if self.degrees == True:
            print "self.x = ", self.x
            self.x = self.x * math.pi / 180
            print "self.x now = ", self.x
            print "self.y = ", self.y
            self.y = self.y * math.pi / 180
            print "self.y now = ", self.y
            #self.z = self.z * math.pi / 180
            self.degrees = False
    def __repr__(self):
        if not self.part == None:
            part_name = self.part.name
        else: part_name = "None"
        return "Interface(name=%s,id=%s,part.name=%s,units=%s,geometry=%s,point=%s,x=%s,y=%s,z=%s)" % (self.name, self.identifier, part_name, self.units, self.geometry, self.point, self.x, self.y, self.z)
    def yaml_repr(self):
        return "name: %s\nidentifier: %s\nhermaphroditic: %s\nunits: %s\ngeometry: %s\npoint: %s\nx: %s\ny: %s\nz: %s\npart: %s" % (self.name, self.identifier, self.hermaphroditic, self.units, self.geometry, self.point, self.x, self.y, self.z, self.part)
