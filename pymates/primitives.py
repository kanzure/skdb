#!/usr/bin/python

import yaml
import numpy

class PrimitiveShape(yaml.YAMLObject):
    '''generic primitive shape wrapper for pythonOCC/OpenCASCADE and friends'''
    yaml_tag = '!PrimitiveShape' #not this matters much
    def __init__(self,x=0,y=0,z=0,i=numpy.array([0,0,0]),j=numpy.array([0,0,0]),k=numpy.array([0,0,0])):
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.j = j
        self.k = k
