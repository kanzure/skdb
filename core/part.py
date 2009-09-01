#!/usr/bin/python
#defines skdb.Part
import yaml
import time
from yamlcrap import FennObject
from interface import Connection
from graph.Digraph import digraph
import os

class Assembly(FennObject, digraph):
    yaml_tag = "!assembly"
    def __init__(self, name=None, description=None, created=time.time()):
        digraph.__init__(self)
    def __eq__(self, other):
        '''two assemblies are equal if each has the same parts and same connections'''
        return True
    #def __repr__
    #def from_yaml
    #def to_yaml
    def add_part(self, part):
        self.add_node(part)
    def remove_part(self, part):
        self.del_node(part)
        #not sure what to do about the stored edges
    def add_connection(self, connection):
        self.add_edge(connection.interface1, connection.interface2)
    def remove_connection(self, connection):
        self.del_edge(connection.interface1, connection.interface2)
    def parts(self):
        '''returns a list of the parts in the assembly graph'''
        return self.nodes()
    def connections(self):
        '''returns a list of the edges in the assembly graph'''
        return self.edges()

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
        return list(rval)
        
    def __add__(self, other): #i'm afraid this metaphor doesn't hold up under scrutiny
        return self.options(other)
        
    def __repr__(self):
        return "%s(name=%s, interfaces=%s)" % (self.__class__.__name__, self.name, self.interfaces)


