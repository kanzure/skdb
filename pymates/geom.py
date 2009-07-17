#!/usr/bin/python

import yaml
import numpy
import primitives

class Circle(primitives.PrimitiveShape):
    '''generic circle. units are meters.'''
    yaml_tag = '!circle'
    def __init__(self,radius=1,x=0,y=0,z=0,i=numpy.array([0,0,0]),j=numpy.array([0,0,0]),k=numpy.array([0,0,0])):
        '''xyz are positions. ijk are unit vectors describing the local coordinate frame.'''
        super(x=x,y=y,z=z,i=i,j=j,k=k)
        self.radius = radius

class Square(primitives.PrimitiveShape):
    '''generic square. units are meters.'''
    yaml_tag = '!square'
    def __init__(self,width=1,height=1,x=0,y=0,z=0,i=numpy.array([0,0,0]),j=numpy.array([0,0,0]),k=numpy.array([0,0,0])):
        super(x=x,y=y,z=z,i=i,j=j,k=k)
        self.width = width
        self.height = height
