#skdb.py
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os
import sys
from string import Template as string_template
from template import Template
from package import Package, package_file, load_package, check_unix_name, PackageSet
from units import Unit, Range, Uncertainty, UnitError, NaNError
from interface import Interface, Connection
from part import Part
from yamlcrap import FennObject, Dummy, tag_hack, add_yaml_resolvers, load
import settings

def prettyfloat(num):                                                                                      
    '''round down to 0 if abs(num) < +-1e-13, gets rid of icky floating point errors'''              
    return str(float("%.13f" % (float(num))))     

def close_enough(num1, num2, tolerance=1e-6):
    if abs(num2 - num1) < tolerance: return True
    else: return False

class Distribution(FennObject):
    yaml_path = ['typical', 'feasible']

class RuntimeSwitch(FennObject):
    '''return different values depending on what parameters have been selected.
    example: !example
        temperature: !which teatype, temp
        parameters:
            teatype:
                iced:
                    flavor: lemon
                    temp: 280K
                hot:
                    flavor: earl grey
                    temp: 340K
    >>> example(teatype=iced) #note this doesnt actually work yet
    >>> example.temperature
    280K'''
    
    yaml_tag = '!which'
    def __init__(self, depends=None, parameter=None): #i dont like 'depends' but cant think of a better word
        self.depends, self.parameter = depends, parameter
    def __repr__(self):
        return 'RuntimeSwitch(%s, %s)' % (self.depends, self.parameter)
    def yaml_repr(self):
        return '%s, %s' % (self.depends, self.parameter)
    def get(self):
        if self.parameter:
            valid_values = package.parameters[self.depends].keys()
            if package.runtime[self.depends] in valid_values: 
                return package.parameters[self.depends][package.runtime[self.depends]][self.parameter] #zoinks
            else: 
                return None 
        else: 
            try: return getattr(package.runtime, self.depends) #uh, this is probably wrong
            except AttributeError: return package[self.depends] #not an object
  #some function to search for similar values here

    @classmethod
    def from_yaml(cls, loader, node):
        '''see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''
        data = loader.construct_scalar(node)
        try: depends, parameter = [i.strip() for i in data.split(',')]
        except ValueError: #only one argument
            depends = data.strip()
            return cls(depends)
        return cls(depends, parameter=parameter)


class Formula(FennObject, str):
    yaml_tag = '!formula'

class Geometry(FennObject):
    yaml_tag = '!geometry'
    
class Process(FennObject):
    yaml_tag = '!process'
    def __init__(self, name=None):
        self.name, self.classification, self.mechanism, self.geometry, self.surface_finish, self.consumables, self.functionality, self.effects, self.parameters, self.safety = None, None, None, None, None, None, None, None, None, None
        self.name = name

    #def __repr__(self):
        #return "Process(%s)" % (self.name)
    

class Material(Package):
    yaml_tag = '!material'
    def __init__(self, name=None, density=1, specific_heat=1, etc=None): #TODO figure out what goes here
        self.name = name
        self.density = density
        self.specific_heat = specific_heat

class Fastener(Package):
    yaml_tag = '!fastener'
    '''could be a rivet, could be a bolt. duct tape? superglue? twine? hose clamp?
    these methods are what actually get called by higher levels of abstraction'''
    def __init__(self, force=None, rigidity=None, safety_factor=7):
        pass

class Component(yaml.YAMLObject):
    '''is this sufficiently generic or what?'''
    yaml_tag = '!component'
    interfaces = []
    #def __init__(self):
    #        pass
    pass

class Bolt(Fastener):
    '''a screw by itself cannot convert torque to force. a bolt is a screw with a nut'''
    def __init__(self, screw=None, nut=None):
        self.screw = screw
        self.nut = nut

add_yaml_resolvers([Range, RuntimeSwitch, Formula, Uncertainty])

def main():
    #basic self-test demo
    load_package('screw')
    package = load(open('tags.yaml'))
    print dump(package)

if __name__ == "__main__":
    main()
