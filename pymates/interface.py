#!/usr/bin/python
#defines pymates.interface.Interface
import yaml

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag = '!interface'
    def __init__(self, name="generic interface name", units=None, geometry=None, point=[0,0,0], x=0, y=0, z=0):
        self.name, self.units, self.geometry, self.point, self.x, self.y, self.z = name, units, geometry, point, x, y, z
    def __repr__(self):
        return "Interface(name=%s,units=%s,geometry=%s,point=%s,x=%s,y=%s,z=%s)" % (self.name, self.units, self.geometry, self.point, self.x, self.y, self.z)
    def yaml_repr(self):
        return "name: %s\nunits: %s\ngeometry: %s\npoint: %s\nx: %s\ny: %s\nz: %s" % (self.name, self.units, self.geometry, self.point, self.x, self.y, self.z)
    #@classmethod
    #def to_yaml(cls, dumper, data):
    #    return dumper.represent_scalar(cls.yaml_tag, cls.yaml_repr(data))
    #@classmethod
    #def from_yaml(cls, loader, node):
    #    return Interface("node name from from_yaml")
