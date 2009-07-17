#!/usr/bin/python
#pymates

import yaml
import re
import geom

# the following aren't our responsibility, actually (pythonOCC?)
#class Circle(yaml.YAMLObject)
#class Cylinder(yaml.YAMLObject)
#class InterfaceGeom(yaml.YAMLObject):

class Part(yaml.YAMLObject):
    '''used for part mating. argh I hope OCC doesn't already implement this and I just don't know it.'''
    yaml_tag = '!part'
    yaml_pattern = re.compile("(.*)")
    def __init__(self, name="generic part"):
        self.name = name
    def __repr__(self):
        return "Part(name=%s)" % (self.name)
    def yaml_repr(self):
       return "not implemented: %s, %s" % (self.name, self.__class__.__name__) #yaml dumps tag automatically
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, cls.yaml_repr(data))
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node)
        return cls(name=data) #better?

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag = '!interface'
    yaml_pattern = re.compile('(.*)')
    def __init__(self, name, units=None, geometry=None):
        self.name = name
        self.units = units
        self.geometry = geometry # need to get a geometry handler class to get everything looking the same
        # TODO: coordinates (location) of an interface
    def __repr__(self):
        return "Interface(name=%s,units=%s,geometry=%s)" % (self.name, self.units, self.geometry)
    def yaml_repr(self):
        return "%s\n not implemented: foo" % (self.name)
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, cls.yaml_repr(data))
    @classmethod
    def from_yaml(cls, loader, node):
        return Interface("node name from from_yaml")

#for cls in [Part, Interface]:
#    yaml.add_implicit_resolver(cls.yaml_tag, cls.yaml_pattern)

def load(foo):
    return yaml.load(foo)
def dump(foo):
    return yaml.dump(foo, default_flow_style=False)

handler = open("models/blockhole.yaml","r")
content = handler.read()
print "loading the file .. it looks like this: ", load(content)
print "dumping the loaded file looks like this: ", dump(load(content))

