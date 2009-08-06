#!/usr/bin/python
from skdb import Part
from string import Template
from interfaces import Stud, AntiStud 

__author__ = "bryan bishop"
__license__ = "GPL2+"
__version__ = "0.0.1"
__maintainer__ = "bryan bishop"
__email__ = "kanzure@gmail.com"
__status__ = "Development"

class Lego(Part):
    '''standard lego part'''
    yaml_tag = "!lego"
    def setup(self, name, num_pegs=0, num_holes=0):
        '''sets up a lego part'''
        self.name = name
        self.interfaces = []
        for each in range(num_holes):
            new_hole = AntiStud(self)
            new_hole.identifier = len(self.interfaces)
            self.interfaces.append(new_hole)
        for each in range(num_pegs):
            new_peg = Stud(self)
            new_peg.identifier = len(self.interfaces)
            self.interfaces.append(new_peg)
    def pegs(self):
        '''returns a list of peg interfaces that this Lego has'''
        results = []
        for each in self.interfaces:
            if each.__class__.__name__ == "Peg":
                results.append(each)
        return results
    def holes(self):
        '''returns a list of hole interfaces that this Lego has'''
        results = []
        for each in self.interfaces:
            if each.__class__.__name__ == "Hole":
                results.append(each)
        return results
    def __repr__(self):
        return "Lego(name=%s, num_pegs=%d, num_holes=%d)" % (self.name, len(self.pegs()), len(self.holes()))

