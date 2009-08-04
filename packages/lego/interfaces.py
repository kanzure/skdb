#!/usr/bin/python
'''this file more or less describes the grammar used for constructing things out of Lego'''
from skdb import Interface
#not done. see http://mr-bucket.co.uk/GLIDE/LCD_File_Format.html#Implimentation

class Feature(Interface):
    @classmethod
    def __repr__(cls):
        if not hasattr(self,"part") or self.part == None:
            part_name = "None"
        else:
            part_name = self.part.name
        return "%s(part=%s,name=%s)" % (cls.__name__, part_name, self.name)

class Edge(Feature):
    def __init__(self):
        self.complement=Edge

class Stud(Feature):
    def __init__(self):
        self.complement = Hole

class Antistud(Feature):
    def __init__(self):
        self.complement = Peg


