#!/usr/bin/python
#this is a "dummy" bearing: it doesn't currently represent a bearing
import skdb
from skdb import Part, Interface, Unit

__author__ = "bryan bishop"
__license__ = "GPL2+"
__version__ = "0.0.1"
__maintainer__ = "bryan bishop"
__email__ = 'kanzure@gmail.com'
__status__ = "Development"

class Bearing(Part):
    yaml_tag = "!bearing"
    '''a screw by itself isn't a fastener, it needs a nut of some sort
    this is a bearing that could be used with a screw
    this bearing is a dummy bearing- do not expect anything from it (yet)'''
    def __init__(self, inner_diameter=Unit("1mm"), outer_diameter=Unit("1mm")):
        #self.inner_diameter, self.outer_diameter = inner_diameter, outer_diameter
        #assert self.inner_diameter.compatible('m')
        #assert self.outer_diameter.compatible('m')
        #compression_face = Interface("compression-face", part=self)
        #other_face = Interface("other-face", part=self)
        #self.interfaces = [compression_face, other_face]
        self.interfacecs = []
        pass
    def post_init_hook(self):
        pass
    def max_force(self):
        '''load bearing can withstand without permanent set, in lbf'''
        return skdb.Unit("400lbf")
  
    def breaking_force(self):
        '''load bearing can withstand without breaking, in lbf'''
        #return skdb.Unit("800lbf")
        pass
