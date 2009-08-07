#!/usr/bin/python
#defines skdb.Part
import yaml
import time
from interface import Mate
from yamlcrap import FennObject

class Part(FennObject):
    '''used for part mating. argh I hope OCC doesn't already implement this and I just don't know it.
    should a part without an interface be invalid?'''
    yaml_tag = '!part'
    def __init__(self, name=None, description=None, created=time.time(), files=[], interfaces=[]):
        if not hasattr(self, "name"):
            self.name = name
        if not hasattr(self, "description"):
            self.description = description
        if not hasattr(self, "created"):
            self.created = created
        if not hasattr(self, "files"):
            self.files = files
        if not hasattr(self, "interfaces"):
            self.interfaces = interfaces
    def makes_sense(self):
        '''checks whether or not this part makes sense
        classes that inherit from Part should have their own makes_sense method.
        returns True if the data loaded up for the part makes sense.
        returns False if the data loaded up for the part does not make sense.
        '''
        return True
    def options(self, part):
        '''what can this part connect to?'''
        interface_list = set(part.interfaces)
        if self in interface_list: interface_list.remove(self) #unless this part is really flexible
        rval = set()
        for interface in interface_list:
                for j in self.interfaces:
                    if interface.compatible(j) and j.compatible(interface):
                        rval.add(Mate(interface, j))
        return rval
    def __add__(self, other):
        return list(self.options(other))
    def __repr__(self):
        return "%s(name=%s, description=%s, created=%s, files=%s, interfaces=%s)" % (self.__class__.__name__, self.name, self.description, self.created, self.files, self.interfaces)

try:
        import OCC.Utils.DataExchange.STEP
        def load_CAD(self):
            '''load this object's CAD file. assumes STEP.'''
            if len(self.files) == 0: return #no files to load
            #FIXME: assuming STEP
            #TODO: check/verify filename path
            #FIXME: does not properly load in models from multiple files (2009-07-30)
            for file in self.files:
                my_step_importer = OCC.Utils.DataExchange.STEP.STEPImporter(str(file))
                my_step_importer.ReadFile()
                self.shapes = my_step_importer.GetShapes()
                self.compound = my_step_importer.GetCompound()
            #i, j, k, point = self.interfaces[0].i, self.interfaces[0].j, self.interfaces[0].k, self.interfaces[0].point
            #x,y,point = self.interfaces[0].x,self.interfaces[0].y,self.interfaces[0].point
            return self.shapes
        Part.load_CAD = load_CAD
        def add_shape(self, result):
            '''add a shape to self.ais_shapes. this isn't as exciting as you think it is.'''
            if type(result) == type([]): self.ais_shapes = result[0]
            else: self.ais_shapes = result
            return
        Part.add_shape = add_shape

except ImportError: print "Couldn't import OCC.Utils.DataExchange.STEP: Is pythonOCC installed properly?"
