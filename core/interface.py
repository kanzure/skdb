#!/usr/bin/python
#defines pymates.interface.Interface
from yamlcrap import FennObject
import math


class Interface(FennObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry. theinterface geometry is located at "point" (in mm for now, sorry) and rotated about its Z vector clockwise "rotation" degrees looking away from the origin. (TODO: verify) The geometry is then rotated such that its Z vector points along "orientation".
    
    an alternative way to specify geometry is with "point" and two vectors: "x_vec" and "y_vec".
    in both cases the mating trajectory is along the Z vector.'''
    yaml_tag = '!interface'
    converted = False
    def __init__(self, name=None, units=None, geometry=None, point=[0,0,0], orientation=[0,0,1], rotation=0, part=None, max_connections=1):
        self.name, self.units, self.geometry, self.part = name, units, geometry, part
        self.point, self.orientation, self.rotation = point, orientation, rotation
        self.max_connections = max_connections
        self.connected = []
        self.identifier = None
        self.complement = None #should be overwritten for specific problem domains
    def is_busy(self):
        if len(self.connected) >= self.max_connections: return True
        else: return False
    def compatible(self, other):
        '''returns True if other is complementary. this method should probably get overwritten for specific problem domains.'''
        for t in self.setify(self.complement):
            if isinstance(other, t): return True
        return False
    def options(self, parts):
        '''what can this interface connect to?'''
        #FIXME: what about options(self,interface)?
        parts = self.setify(parts) #yay sets!
        if self.part in parts: parts.remove(self.part) #unless it's really flexible
        rval = set()
        for part in parts:
            for i in part.interfaces:
                if i.compatible(self) and self.compatible(i):
                    if not i.is_busy() and not self.is_busy():
                        rval.add(Connection(self,i))
        return rval     
    def __repr__(self):
        if not self.part == None:
            part_name = self.part.name
        else: part_name = None
        return 'Interface("%s", part="%s")' % (self.name, part_name)

class Connection:
    '''a temporary scenario to see if we should connect these two interfaces'''
    def __init__(self, interface1, interface2):
        assert hasattr(interface1, 'connected')
        assert hasattr(interface2, 'connected')
        self.interface1 = interface1
        self.interface2 = interface2
        
    def connect(self):
        self.interface1.connected.add(self)
        self.interface2.connected.add(self)
        return
        
    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.interface1, self.interface2)
        
    def makes_sense(self): #should we include is_busy()?
        return self.interface1.compatible(self.interface2) and self.interface2.compatible(self.interface1)
      
#from geom import Mate
#try: from skdb.paths import Mate
#except ImportError:      
class Mate(Connection):
        pass