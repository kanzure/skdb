#!/usr/bin/python
#defines pymates.interface.Interface
import yaml
import math

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag = '!interface'
    def __init__(self, name="generic interface name", units=None, geometry=None, point=[0,0,0], x=0, y=0, z=0):
        '''rotate first about x, then about z. give x and z in degrees (__init__ autoconverts to radians)'''
        self.name, self.units, self.geometry, self.point, self.x, self.y, self.z = name, units, geometry, point, x*math.pi/180, y*math.pi/180, z*math.pi/180
    def __repr__(self):
        return "Interface(name=%s,units=%s,geometry=%s,point=%s,x=%s,y=%s,z=%s)" % (self.name, self.units, self.geometry, self.point, self.x, self.y, self.z)
    def yaml_repr(self):
        return "name: %s\nunits: %s\ngeometry: %s\npoint: %s\nx: %s\ny: %s\nz: %s" % (self.name, self.units, self.geometry, self.point, self.x, self.y, self.z)
