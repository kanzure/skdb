#skdb.py
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os
from string import Template

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
    
sci = '([+-]?\d*.?\d+([eE][+-]?\d+)?)' #exp group leaves turds.. better way to do regex without parens?

class FennObject(yaml.YAMLObject):
    '''so i dont repeat generic yaml stuff everywhere'''
    def __setstate__(self, attrs):
        for (k,v) in attrs.items():
            k = re.sub(' ', '_', k) #replace spaces with underscores because "foo.the attr" doesn't work
            self.__setattr__(k,v)
    @classmethod
    def to_yaml(cls, dumper, data):
        if hasattr(cls, 'yaml_repr'):
            tmp = cls.yaml_repr(data)
            return dumper.represent_scalar(cls.yaml_tag, tmp)
        else: 
            #i want to return the default yaml dump; but how?       
            #cls.to_yaml = yaml.YAMLObject.to_yaml
            #return cls.to_yaml(dumper, data)
            ##return dumper.represent_mapping(cls.yaml_tag, data)
            tmp = cls.__repr__(data)
            return dumper.represent_scalar(cls.yaml_tag, tmp)

    @classmethod
    def from_yaml(cls, loader, node):
        '''see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''
        data = loader.construct_scalar(node)
        if hasattr(cls, 'yaml_pattern') and hasattr(cls, 'yaml_parse_args') and cls.yaml_parse_args == True:
            match = re.search(cls.yaml_pattern, data)
            if match:
                return cls(match.groups()) #i guess this will stuff the regex groups into the positional args #TODO unit test
        else:
            return cls(data)

class Range(FennObject):
    yaml_tag = "!range"
    #expression should look something like: 1e4 m .. 2km
    yaml_pattern = sci+'\s*(\D?.*)?\s*\.\.\s*'+sci+'\s*(\D?.*)$'
    def __init__(self, min, max):
        self.min = min
        self.max = max
    def __repr__(self):
        return "Range(%s, %s)" %(self.min, self.max)
    def yaml_repr(self):
        return "%s .. %s" %(self.min, self.max)
    def __eq__(self, other):
        if type(other) == type(self):
            return self.min == other.min and self.max == other.max
        else: return None
    @classmethod
    def from_yaml(cls, loader, node):
        '''see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''
        data = loader.construct_scalar(node)
        match = re.search(cls.yaml_pattern, data)
        a, crap, units1, b, crap2, units2 = match.groups() 
        if units2 != '':
            if units1 != '':
                a = Unit(a+units1)
                b = Unit(b+units2)
            else:
                a = Unit(a+units2)
                b = Unit(b+units2)
        else: 
            #double yuck. maybe i should just pass this to units instead?
            a = eval(a)
            b = eval(b)
        return cls(min(a,b), max(a,b))

class Distribution(FennObject):
    yaml_path = ['typical', 'feasible']

#unum looks rather immature, perhaps I will write a wrapper for GNU units instead
#scientific.Physics.PhysicalQuantities looks ok-ish        
class UnitError(Exception): pass 
class NaNError(Exception): pass


#build the new db for our custom units
f1 = open('/usr/share/misc/units.dat').read()
f2 = open('supplemental_units.dat').read()
f3 = open('combined.dat', 'w')
f3.write(f1+f2)
f3.close()

class Unit(FennObject):
    yaml_tag = "!unit"
    '''try to preserve the original units, and provide a wrapper to the GNU units program'''
    units_call = "units -f combined.dat -t " #export LOCALE=en_US; ?
    def __init__(self, string):
        #simplify(string) #check if we have a good unit format to begin with. is there a better way to do this?
        self.string = str(string)
        self.simplify() #has no side effects, just raise any exceptions early
        #e_number = '([+-]?\d*\.?\d*([eE][+-]?\d+)?)' #engineering notation
        #match = re.match(e_number + '?(\D*)$', string) #i dunno wtf i was trying to do here
        #match = re.match(e_number + '?(.*)$', string)
        #if match is None: raise UnitError, string
        #try: self.number = float(match.group(1))
        #except ValueError: self.number = 1.0
        #self.unit = match.group(3)

    def __repr__(self):
        return str(self.string)
    
    def yaml_repr(self):
        if hasattr(self, 'uncertainty'): u = self.uncertainty.yaml_repr() #TODO delete this
        else: u = ''
        return self.string +u

    @staticmethod #is this right?
    def sanitize(string):
        '''intercept things that will cause GNU units to screw up'''
        if hasattr(string, 'string'): string = string.string #egads. in case i accidentally pass a Unit or something
        if string is None or str(string) == 'None' or str(string) == '()': string = 0  
        for i in ['..', '--']:
            if str(string).__contains__(i):
                raise UnitError, "Typo? units expression '"+ string + "' contains '" + i + "'"
        return '('+str(string)+')' #units -1 screws up; units (-1) works

    def units_happy(self, call_string, rval):
        '''the conversion or expression evaluated without error'''
        error = re.search('Unknown|Parse|Error|invalid|error', rval)
        if error:  
            raise UnitError, str(call_string) + ': ' + str(rval)
        nan = re.search('^nan', rval) #not sure how to not trip on results like 'nanometer'
        if nan:
            raise NaNError, rval
        return True #well? what else am i gonna do

    def units_operator(self, a, b, operator):
        if str(a)=='None' or str(b)=='None': return None
        s = Template('($a)$operator($b)')
        expression = s.safe_substitute(a=str(a), b=str(b), operator=str(operator))
        rval = Unit(expression)
        if debug: rval.check()
        return rval
    
    def __mul__(self, other):
        return self.units_operator(self, other, '*')
    __rmul__ = __mul__

    def __div__(self, other):
        return self.units_operator(self, other, '/')
    __rdiv__ = __div__

    def __add__(self, other):
        return self.units_operator(self, other, '+')
    __radd__ = __add__

    def __sub__(self, other):
        return self.units_operator(self, other, '-')
    __rsub__ = __sub__
    
    def __eq__(self, other):
        if hasattr(other, 'string'): other = other.string
        if self.simplify() == Unit(other).simplify(): return True
        else: return False
    
    def __ne__(self, other):
        if self.__eq__(other): return True
        else: return False
    
    def __cmp__(self, other):
        #i should probably be using __lt__, __gt__, etc
        #neither does this work for nonlinear units like tempF() or tempC()
        if self.compatible(other):
            conv = self.conv_factor(other)
            #print conv #god what a mess
            if conv == 1: return 0
            if conv < 1 and conv > 0: return -1
            if conv > 1: return 1
            if conv <0 and conv > -1: return -1
            if conv <-1 : return 1
            if conv == -1: return 1
            if conv == inf: return 1
            if conv == 0: return -1
    
    def conv_factor(self, destination):
        '''the multiplier to go from one unit to another, for example from inch to mm is 25.4'''
        conv_factor = os.popen(self.__class__.units_call + "'" + self.sanitize(self.string) + "' '" + self.sanitize(destination) + "'").read().rstrip('\n')
        if self.units_happy(self.string, conv_factor): 
            return float(conv_factor)
        else: raise UnitError, conv_factor, destination
        
    def convert(self, destination):
        if self.compatible(destination):
            return str(self.conv_factor(destination)) +'*'+ str(destination) #1*mm
        
    def to(self, dest):
            return Unit(self.convert(dest))
    
    def simplify(self, string=None):
        '''returns a string'''
        if string is None: string = self.string
        rval = os.popen(self.__class__.units_call + "'" + self.sanitize(string) + "'").read().rstrip('\n')
        if self.units_happy(string, rval): return rval
        else: raise UnitError, self.string

    def check(self):
        try: self.simplify()
        except UnitError or NaNError: return False
        return True

    def simplified(self):
        '''returns a Unit in simplified format. note that it may actually look more complicated due to the lack of default units'''
        return Unit(self.simplify())
    
    def compatible(self, other):
        '''check if both expressions boil down to the same base units'''
        try: self.simplify(self.string + '+' + self.sanitize(other))
        except UnitError: return False
        else: return True

    def number(self): 
        '''return the number portion of the unit string'''
        return 'not yet implemented, sorry!'
    def unit(self):
        '''return the unit portion of the unit string'''
        return 'not yet implemented, sorry!'

class Uncertainty(Unit):
    '''predicted range of error in the measurement'''
    yaml_tag = "!uncertainty" #ehh.. going to do something with this eventually
    yaml_pattern = '^\+-' + sci + '\s*(\D?.*)$' #+-, number, units
    def __init__(self, string):
        match = re.match('^\+-(.*)', string)
        if match: unit = match.group(1)
        else: raise SyntaxError, "'"+ string +"'" + ": uncertainty must begin with +-, for now at least" #got any better ideas?
        Unit.__init__(self, unit)
    def __repr__(self):
        return 'Uncertainty('+ Unit.__repr__(self) +')'
    def yaml_repr(self):
        return "+-%s" % (self.string)


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
