#!/usr/bin/python
#defines skdb.Part
import yaml
import time
from yamlcrap import FennObject
from interface import Connection
import os

class Part(FennObject):
    '''used for part mating. argh I hope OCC doesn't already implement this and I just don't know it.
    should a part without an interface be invalid?'''
    yaml_tag = '!part'
    transformation = None
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
            for interface in interfaces:
                interface.part = self

    def post_init_hook(self):
        for i in self.interfaces:
            i.part = self #so we dont have to do this over and over in the data.yaml
            i.connected = []
    def makes_sense(self):
        '''checks whether or not this part makes sense
        classes that inherit from Part should have their own makes_sense method.
        returns True if the data loaded up for the part makes sense.
        returns False if the data loaded up for the part does not make sense.
        '''
        raise NotImplementedError
        
    def options(self, parts):
        '''what can this part connect to?'''
        parts = self.setify(parts)
        if self in parts: parts.remove(self) #unless this part is really flexible
        for part in parts:
            interfaces = set(part.interfaces)
            rval = set()
            for i in interfaces:
                    for j in self.interfaces:
                        if i.compatible(j) and j.compatible(i):
                            rval.add(Connection(i, j))
        return rval
        
    def __add__(self, other):
        return list(self.options(other))
        
    def __repr__(self):
        return "%s(name=%s, interfaces=%s)" % (self.__class__.__name__, self.name, self.interfaces)


