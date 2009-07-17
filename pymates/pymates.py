#!/usr/bin/python
#pymates

import yaml
import re
import time
import geom

# the following aren't our responsibility, actually (pythonOCC?)
#class Circle(yaml.YAMLObject)
#class Cylinder(yaml.YAMLObject)
#class InterfaceGeom(yaml.YAMLObject):

class Part(yaml.YAMLObject):
    '''used for part mating. argh I hope OCC doesn't already implement this and I just don't know it.'''
    yaml_tag = '!part'
    yaml_pattern = re.compile("(.*)")
    def __init__(self, description="description", created=time.localtime(), files=[], interfaces={}):
        self.description, self.created, self.files, self.interfaces = description, created, files, interfaces
    def __repr__(self):
        return "%s(description=%s, created=%s, files=%s, interfaces=%s)" % (self.__class__.__name__, self.description, self.created, self.files, self.interfaces)
    def yaml_repr(self):
       return "description: %s\ncreated: %s\nfiles: %s\ninterfaces: %s" % (self.description, self.created, self.files, self.interfaces)
    def __setstate__(self, attrs):
        #print "Part.__setstate__ says attrs = ", attrs
        for (k,v) in attrs.items():
            #self.__setattr__(each[0],each[1])
            if type(v) == Interface:
                v.name = k
                if hasattr(self, "interfaces"): self.interfaces[k] = v
                else:
                    self.interfaces = {}
                    self.interfaces[k] = v
                #self.interfaces[k] = v
            self.__setattr__(k,v)
    #@classmethod
    #def to_yaml(cls, dumper, data):
    #    return dumper.represent_mapping(cls.yaml_tag, cls.yaml_repr(data))
    #@classmethod
    #def from_yaml(cls, loader, node):
    #    print "from_yaml() says that loader = ", loader
    #    data = loader.construct_mapping(node)
    #    print "from_yaml() says that data = ", data
    #    return cls(data)

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag = '!interface'
    yaml_pattern = re.compile('(.*)')
    def __init__(self, name="generic interface name", units=None, geometry=None):
        self.name = name
        self.units = units
        self.geometry = geometry # need to get a geometry handler class to get everything looking the same
        # TODO: coordinates (location) of an interface
    def __repr__(self):
        return "Interface(name=%s,units=%s,geometry=%s)" % (self.name, self.units, self.geometry)
    def yaml_repr(self):
        return "name: %s\nunits: %s\ngeometry: %s" % (self.name, self.units, self.geometry)
    #@classmethod
    #def to_yaml(cls, dumper, data):
    #    return dumper.represent_scalar(cls.yaml_tag, cls.yaml_repr(data))
    #@classmethod
    #def from_yaml(cls, loader, node):
    #    return Interface("node name from from_yaml")

#for cls in [Part, Interface]:
#    yaml.add_implicit_resolver(cls.yaml_tag, cls.yaml_pattern)

def compatibility(part1, part2):
    '''find all possible combinations of part1 and part2 (for each interface/port) and check each compatibility'''
    pass
def compatibility(part1port, part2port):
    '''note that an interface/port object refers to what it is on. so you don't have to pass the parts.'''
    pass

def load(foo):
    return yaml.load(foo)
def dump(foo):
    return yaml.dump(foo, default_flow_style=False)

print "loading the file .. it looks like this: "
print load(open("models/blockhole.yaml"))["blockhole"]
#print "dumping the loaded file looks like this: ", dump(load(content))
