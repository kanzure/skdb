#!/usr/bin/python
#defines pymates.part.Part
import yaml
import time
import OCC.Utils.DataExchange.STEP

class Part(yaml.YAMLObject):
    '''used for part mating. argh I hope OCC doesn't already implement this and I just don't know it.
    should a part without an interface be invalid?'''
    yaml_tag = '!part'
    def __init__(self, name="part name", description="description", created=time.localtime(), files=[], interfaces={}):
        self.name, self.description, self.created, self.files, self.interfaces = name, description, created, files, interfaces
    def load_CAD(self):
        if len(self.files) == 0: return #no files to load
        #FIXME: assuming STEP
        #TODO: check/verify filename path
        for file in self.files:
            my_step_importer = OCC.Utils.DataExchange.STEP.STEPImporter(str(file))
            my_step_importer.ReadFile()
            self.shapes = my_step_importer.GetShapes()
            self.compound = my_step_importer.GetCompound()
        #i, j, k, point = self.interfaces[0].i, self.interfaces[0].j, self.interfaces[0].k, self.interfaces[0].point
        x,z,point = self.interfaces[0].x,self.interfaces[0].z,self.interfaces[0].point
        return self.shapes
    def add_shape(self, result):
        if type(result) == type([]): self.ais_shapes = result[0]
        else: self.ais_shapes = result
        return
    def __repr__(self):
        return "%s(name=%s, description=%s, created=%s, files=%s, interfaces=%s)" % (self.__class__.__name__, self.name, self.description, self.created, self.files, self.interfaces)
    def yaml_repr(self):
       return "name: %s\ndescription: %s\ncreated: %s\nfiles: %s\ninterfaces: %s" % (self.name, self.description, self.created, self.files, self.interfaces)
    #def __setstate__(self, attrs):
        ##print "Part.__setstate__ says attrs = ", attrs
        #for (k,v) in attrs.items():
            ##self.__setattr__(each[0],each[1])
            #if type(v) == Interface:
                #v.name = k
                #if hasattr(self, "interfaces"): self.interfaces[k] = v
                #else:
                    #self.interfaces = {}
                    #self.interfaces[k] = v
            #self.__setattr__(k,v)
    #@classmethod
    #def to_yaml(cls, dumper, data):
    #    return dumper.represent_mapping(cls.yaml_tag, cls.yaml_repr(data))
    #@classmethod
    #def from_yaml(cls, loader, node):
    #    print "from_yaml() says that loader = ", loader
    #    data = loader.construct_mapping(node)
    #    print "from_yaml() says that data = ", data
    #    return cls(data)
