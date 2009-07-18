#!/usr/bin/python
#pymates

#see ~/local/pythonOCC/samples/Level2/DataExchange/import_step_multi.py
#see ~/local/pythonOCC/samples/Level1/TopologyTransformation/mirror.py

import yaml
import re
import time
import geom
#import numpy
import OCC.gp
import OCC.BRepPrimAPI
import OCC.BRepBuilderAPI
import OCC.Display.wxSamplesGui
import OCC.Utils.DataExchange.STEP

# the following aren't our responsibility, actually (pythonOCC?)
#class Circle(yaml.YAMLObject)
#class Cylinder(yaml.YAMLObject)
#class InterfaceGeom(yaml.YAMLObject):

class Part(yaml.YAMLObject):
    '''used for part mating. argh I hope OCC doesn't already implement this and I just don't know it.
    should a part without an interface be invalid?'''
    yaml_tag = '!part'
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
    def __init__(self, name="generic interface name", units=None, geometry=None, point=[0,0,0], i=[0,0,0], j=[0,0,0], k=[0,0,0]):
        self.name, self.units, self.geometry, self.point, self.i, self.j, self.k = name, units, geometry, points, i, j, k
    def __repr__(self):
        return "Interface(name=%s,units=%s,geometry=%s,point=%s,i=%s,j=%s,k=%s)" % (self.name, self.units, self.geometry, self.point, self.i, self.j, self.k)
    def yaml_repr(self):
        return "name: %s\nunits: %s\ngeometry: %s\npoint: %s\ni: %s\nj: %s\nk: %s" % (self.name, self.units, self.geometry, self.point, self.i, self.j, self.k)
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
    return []
def compatibility(part1port, part2port):
    '''note that an interface/port object refers to what it is on. so you don't have to pass the parts.'''
    return []

def load(foo):
    return yaml.load(foo)
def dump(foo):
    return yaml.dump(foo, default_flow_style=False)
def demo(event=None):
    print "loading the file .. it looks like this:"
    blockhole = load(open("models/blockhole.yaml"))["blockhole"]
    print "blockhole is = ", dump(blockhole)
def load_cad_file(event=None, filename="models/plank-with-pegs.step"):
    my_step_importer = OCC.Utils.DataExchange.STEP.STEPImporter(filename)
    my_step_importer.ReadFile()
    the_shapes = my_step_importer.GetShapes()
    the_compound = my_step_importer.GetCompound()
    OCC.Display.wxSamplesGui.display.DisplayShape(the_shapes)
def mate_parts(event=None):
    #mate all of the parts in the workspace
    pass
def exit(event=None):
    import sys; sys.exit()

if __name__ == '__main__':
    OCC.Display.wxSamplesGui.add_menu("do stuff")
    OCC.Display.wxSamplesGui.add_function_to_menu('do stuff', demo)
    OCC.Display.wxSamplesGui.add_function_to_menu('do stuff', load_cad_file)
    OCC.Display.wxSamplesGui.add_function_to_menu('do stuff', mate_parts)
    OCC.Display.wxSamplesGui.add_function_to_menu('do stuff', exit)
    OCC.Display.wxSamplesGui.start_display()
