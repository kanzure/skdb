#skdb.py
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os
from string import Template

from units import Unit, Range, Uncertainty, UnitError, NaNError
from yamlcrap import FennObject

debug = False

# the following aren't our responsibility, actually (pythonOCC?)
#class Circle(yaml.YAMLObject)
#class Cylinder(yaml.YAMLObject)
#class InterfaceGeom(yaml.YAMLObject):

class Interface(yaml.YAMLObject):
    '''"units" should be what is being transmitted through the interface, not about the structure.
    a screw's head transmits a force (N), but not a pressure (N/m**2) because the m**2 is actually interface geometry'''
    yaml_tag='!interface'
    def __init__(self, name, units=None, geometry=None):
        self.name = name
        self.units = units
        self.geometry = geometry # need to get a geometry handler class to get everything looking the same
        # TODO: coordinates (location) of an interface
        
class Contributor(yaml.YAMLObject):
    '''used in package metadata'''
    yaml_tag='!contributor'
    def __init__(self, name, email=None, url=None):
        self.name = name
        self.email = email
        self.url = url

class Author(Contributor):
    yaml_tag='!author'

class Package(yaml.YAMLObject):
    yaml_tag='!package'
    def __init__(self, name, unix_name=None, license=None, urls=None, contributors=None):
        self.name =name
        self.unix_name =unix_name # TODO: complain if it's not a valid "unix name"
        self.license = license
        self.urls = urls
        self.contributors = contributors
        self.contents = {}
        #TODO inherit from some pretty container class




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
    def __init__(self, depends, parameter=None): #i dont like 'depends' but cant think of a better word
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
    
class Process: #(FennObject):
    yaml_tag = '!process'
    def __init__(self, name):
        self.name, self.classification, self.mechanism, self.geometry, self.surface_finish, self.consumables, self.functionality, self.effects, self.parameters, self.safety = None, None, None, None, None, None, None, None, None, None
        self.name = name

    #def __repr__(self):
        #return "Process(%s)" % (self.name)
    

class Material(Package):
    yaml_tag = '!material'
    def __init__(self, name, density=1, specific_heat=1, etc=None): #TODO figure out what goes here
        self.name = name
        self.density = density
        self.specific_heat = specific_heat

class Fastener(Package):
    yaml_tag = '!fastener'
    '''could be a rivet, could be a bolt. duct tape? superglue? twine? hose clamp?
    these methods are what actually get called by higher levels of abstraction'''
    def __init__(self, force, rigidity, safety_factor=7):
        pass

class Thread(Package):
    yaml_tag = '!thread'
    '''examples: ballscrews, pipe threads, bolts - NOT any old helix'''
    def __init__(self, diameter, pitch, gender='male', length=None, form="UN"):
        self.diameter, self.pitch, self.form = Unit(diameter), Unit(pitch), form
        self.gender, self.length, self.form
        self.interfaces = [
                (pitch_diameter, 'in'), # conversion function .. so this is wrong.
                (minor_diameter, 'in'),
                (clamping_force, 'lbf')]
    def pitch_diameter(self):
        assert self.form=="UN" and Unit(self.pitch).compatible('rev/inch'), "this only works for triangular threads atm"
        s = Template('($diameter)-0.6495919rev/($pitch)') #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(string).to('in')
  
    def minor_diameter(self):
        assert self.form=="UN" and Unit(self.pitch).compatible('rev/inch'), "this only works for triangular threads atm"
        s = Template('($diameter)-1.299038rev/($pitch)')  #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(string).to('in')
    
    def clamping_force(self, torque, efficiency=0.1):
        s = Template('($torque)*($pitch)*$efficiency')
        string = s.safe_substitute(torque=torque, pitch=self.pitch, efficiency=efficiency) #fill in template keywords
        force = Unit(string).to('lbf') #I guess this looks better than kg*m/s^2, but there should be a default units setting somewhere
        return force
  
    def tensile_area(self):
        assert Unit(self.pitch).compatible('rev/inch')
        s = Template('pi/4*(($Dm+$Dp)/2)^2') #machinery's handbook 27ed page 1502 formula 9 "tensile-stress area of screw thread"
        string = s.safe_substitute(Dm=self.minor_diameter(), Dp=self.pitch_diameter())
        return Unit(string).to('in^2')
  #max torque requires finding the combined "von mises" stress, given on page 1498
  #because the screw body will twist off as a combination of tensile and torque shear loads

class Component(yaml.YAMLObject):
    '''is this sufficiently generic or what?'''
    yaml_tag = '!component'
    interfaces = []
    #def __init__(self):
    #        pass
    pass

class Bolt(Fastener):
    '''a screw by itself cannot convert torque to force. a bolt is a screw with a nut'''
    def __init__(self, screw, nut):
        self.screw = screw
        self.nut = nut

def load(string):
    for cls in [Range, RuntimeSwitch, Formula, Uncertainty]: #only one at a time works so far?
        if hasattr(cls, 'yaml_pattern'):
            yaml.add_implicit_resolver(cls.yaml_tag, re.compile(cls.yaml_pattern))
    return yaml.load(string)

def dump(value, filename=None):
    retval = yaml.dump(value, default_flow_style=False)
    if filename is not None:
        f = open(filename, 'w')
        f.write(retval)
    else:
        return retval
    #some stdout call here might not be a bad idea

package = 'blah'
def main():
    #basic self-test demo
    package = load(open('tags.yaml'))
    print dump(package)

if __name__ == "__main__":
    main()
