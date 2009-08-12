#!/usr/bin/python
from skdb import Part
from string import Template
from interfaces import grammar, Feature

__author__ = "bryan bishop"
__license__ = "GPL2+"
__version__ = "0.0.1"
__maintainer__ = "bryan bishop"
__email__ = "kanzure@gmail.com"
__status__ = "Development"

class Lego(Part):
    '''standard lego part'''
    yaml_tag = "!lego"
    def __init__(self, name=None, num_pegs=0, num_holes=0):
        self.name = name
        self.interfaces = []
        for each in range(num_holes):
            new_hole = grammar['anti stud']
            import yaml
            print yaml.dump(new_hole)
            print new_hole
            new_hole.identifier = len(self.interfaces)
            self.interfaces.append(new_hole)
        for each in range(num_pegs):
            new_peg = grammar['stud']
            new_peg.identifier = len(self.interfaces)
            self.interfaces.append(new_peg)
    def pegs(self):
        '''returns a list of peg interfaces that this Lego has'''
        results = []
        for each in self.interfaces:
            if each.type == "stud":
                results.append(each)
        return results
    def holes(self):
        '''returns a list of hole interfaces that this Lego has'''
        results = []
        for each in self.interfaces:
            if each.type == "antistud":
                results.append(each)
        return results
    def __repr__(self):
        return "%s(name=%s, num_pegs=%d, num_holes=%d)" % (self.__class__.__name__, self.name, len(self.pegs()), len(self.holes()))

