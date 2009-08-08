#!/usr/bin/python
#defines pymates.interface.Interface
import yaml
import math

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag = '!interface'
    converted = False
    def __init__(self, name=None, units=None, geometry=None, point=[0,0,0], orientation=[0,0,1], rotation=0, part=None, max_connections=1):
        self.name, self.units, self.geometry, self.part = name, units, geometry, part
        self.point, self.orientation, self.rotation = point, orientation, rotation
        self.max_connections = max_connections
        self.connected = None
        self.identifier = None
        self.complement = None #should be overwritten for specific problem domains
    def is_busy(self):
        if self.connected >= self.max_connections: return True
        else: return False
    def compatible(self, other):
        '''returns True if other is complementary. this method should probably get overwritten for specific problem domains.'''
        if self.complement == other.__class__.__name__:
            return True
        else: return False
    def options(self, parts):
        '''what can this interface connect to?'''
        #FIXME: what about options(self,interface)?
        parts = set(parts) #yay sets!
        if self.part in parts: parts.remove(self.part) #unless it's really flexible
        rval = set()
        for part in parts:
            for i in part.interfaces:
                if i.compatible(self) and self.compatible(i):
                    if not i.is_busy() and not self.is_busy():
                        rval.add(Mate(i, self))
        return rval     
    def __repr__(self):
        if not self.part == None:
            part_name = self.part.name
        else: part_name = None
        return 'Interface("%s", part="%s")' % (self.name, part_name)
    def yaml_repr(self):
        return "name: %s\nidentifier: %s\nhermaphroditic: %s\nunits: %s\ngeometry: %s\npoint: %s\nx: %s\ny: %s\nz: %s\npart: %s" % (self.name, self.identifier, self.hermaphroditic, self.units, self.geometry, self.point, self.x, self.y, self.z, self.part)

class Connection:
    '''a temporary scenario to see if we should connect these two interfaces'''
    def __init__(self, interface1, interface2):
        assert hasattr(interface1, 'connected')
        assert hasattr(interface2, 'connected')
        self.interface1 = interface1
        self.interface2 = interface2
    def connect(self):
        self.interface1.connected = self
        self.interface2.connected = self
        return
    def __repr__(self):
        return "Connection(%s, %s)" % (self.interface1, self.interface2)

class Mate(Connection):
    def apply(self):
        '''apply this option for mating'''
    def makes_sense(self):
        return 1
    def __repr__(self):
        return "Mating(%s, %s)" % (self.interface1, self.interface2)
