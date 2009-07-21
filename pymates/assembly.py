#!/usr/bin/python
import yaml

class Assembly(yaml.YAMLObject):
    '''represents a particular 'mate' between two given interfaces on two different parts.'''
    def __init__(self, part1, part2, part1_interface, part2_interface):
        pass
    def __repr__(self):
        pass
    def yaml_repr(self):
        pass
