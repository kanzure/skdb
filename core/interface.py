#!/usr/bin/python
#defines pymates.interface.Interface
import yaml
import math

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag = '!interface'
    def __init__(self, name=None, units=None, geometry=None, point=[0,0,0], x=0, y=0, z=0, part=None, max_connections=1):
        '''rotate first about x, then about z. give x and z in degrees (__init__ autoconverts to radians)'''
        self.name, self.units, self.geometry, self.degrees, self.part = name, units, geometry, False, part
        self.point, self.x, self.y, self.z = point, x, y, z
        self.max_connections = max_connections
        self.connected = None
        self.identifier = None
    def is_busy(self):
        '''really really generic: it's compatible if it's the first one'''
        if self.connected >= self.max_connections: return True
        else: return False
    def compatible(self, other):
        return True #i guess. this should get overwritten for specific problem domains
    def options(self, parts):
        '''what can this interface connect to?'''
        parts = set(parts) #yay sets!
        if self.part in parts: parts.remove(self.part) #unless it's really flexible
        rval = set()
        for part in parts:
            for i in part.interfaces:
                if i.compatible(self) and self.compatible(i):
                    if not i.is_busy() and not self.is_busy():
                        rval.add(Mate(i, self))
        return rval     
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
    '''wtf is a Mate anyway? presumably there's some geometry involved?'''
    def __repr__(self):
        return "Mate(%s, %s)" % (self.interface1, self.interface2)
