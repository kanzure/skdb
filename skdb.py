#skdb.py
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os
from string import Template
import re
import copy

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

class Range(yaml.YAMLObject):
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
        return self.__repr__()
    def __eq__(self, other):
        if type(other) == type(self):
            return self.min == other.min and self.max == other.max
        else: return None
    @classmethod #constructor takes class as first argument
    def constructor(cls, data): 
        '''see http://pyyaml.org/wiki/PyYAMLDocumentation#Constructorsrepresentersresolvers'''
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
 
class Uncertainty(yaml.YAMLObject):
    '''predicted range of error in the measurement'''
    yaml_tag = "!uncertainty" #ehh.. going to do something with this eventually
    yaml_pattern = '^\+-' + sci + '\s*(\D?.*)$' #+-, number, units
    def __init__(self,value):
        self.value = Unit(value)
    def yaml_repr(self):
        if self.value is not None:
            return "+-%s" % (self.value)
        else: return ""
        
    @classmethod
    def constructor(cls, data):
        match = re.search(cls.yaml_pattern, data)
        if match is None:
            print 'why am i here?'
            print "name: %s, pattern: %s, data: %s" %(cls.__name__, cls.yaml_pattern, data)
            return None
        number = match.group(1) #cast to float here?
        assert float(number) >= 0 #negative uncertainty would be highly unusual
        units = match.group(3) #3 because scientific notation regex has 2 groups in it
        return cls(number+units)


#unum looks rather immature, perhaps I will write a wrapper for GNU units instead
#scientific.Physics.PhysicalQuantities looks ok-ish        
class UnitError(Exception): pass 
class NaNError(Exception): pass

#first you need to do this:
#cat /usr/share/misc/units.dat > combined.dat
#cat supplemental_units.dat >> combined.dat
units_call = "units -f combined.dat -t " #export LOCALE=en_US; ?
def sanitize(string):
    '''intercept things that will cause GNU units to screw up'''
    if string is None or str(string) == 'None' or str(string) == '()': string = 0  
    for i in ['..', '--']:
        if str(string).__contains__(i):
            raise UnitError, "Typo? units expression '"+ string + "' contains '" + i + "'"
    return '('+str(string)+')' #units -1 screws up; units (-1) works

def units_happy(call_string, rval):
    '''the conversion or expression evaluated without error'''
    error = re.search('Unknown|Parse|Error|invalid|error', rval)
    if error:  
        raise UnitError, str(call_string) + ': ' + str(rval)
    nan = re.search('^nan', rval) #not sure how to not trip on results like 'nanometer'
    if nan:
        raise NaNError, rval
    return True #well? what else am i gonna do

def simplify(string):
    rval = os.popen(units_call + "'" + sanitize(string) + "'").read().rstrip('\n')
    if units_happy(string, rval): return rval
    else: raise UnitError

def conv_factor(string, destination):
    '''the multiplier to go from one unit to another, for example from inch to mm is 25.4'''
    conv_factor = os.popen(units_call + "'" + sanitize(string) + "' '" + sanitize(destination) + "'").read().rstrip('\n')
    if units_happy(string, conv_factor): 
        return float(conv_factor)
    else: raise UnitError, conv_factor, destination
    
def convert(string, destination):
    return str(conv_factor(string, destination)) +'*'+ str(destination) #1*mm
    
def check(string):
        try: simplify(str(string))
        except UnitError or NaNError: return False
        return True

def compatible(a, b):
    '''check if both expressions boil down to the same base units'''
    try: simplify(str(a) + '+' + str(b))
    except UnitError: return False
    else: return True

class Unit(yaml.YAMLObject):
    yaml_tag = "!unit"
    '''try to preserve the original units, and provide a wrapper to the GNU units program'''
    def __init__(self, string, uncertainty=None):
        simplify(string) #check if we have a good unit format to begin with. is there a better way to do this?
        self.string = str(string)
        if uncertainty is not None:
            self.uncertainty = Uncertainty(uncertainty)
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
        if hasattr(self, 'uncertainty'): u = self.uncertainty.yaml_repr()
        else: u = ''
        return self.string +u

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
        if str(simplify(self)) == str(simplify(other)): return True
        else: return False
    
    def __ne__(self, other):
        if self.__eq__(other): return True
        else: return False
    
    def __cmp__(self, other):
        #i should probably be using __lt__, __gt__, etc
        #neither does this work for nonlinear units like tempF() or tempC()
        if self.compatible(other):
            conv = conv_factor(self, other)
            #print conv #god what a mess
            if conv == 1: return 0
            if conv < 1 and conv > 0: return -1
            if conv > 1: return 1
            if conv <0 and conv > -1: return -1
            if conv <-1 : return 1
            if conv == -1: return 1
            if conv == inf: return 1
            if conv == 0: return -1
    
    def to(self, dest):
        return Unit(convert(self, dest))
    
    def check(self):
        return check(self)

    def simplify(self):
        return Unit(simplify(self))
    
    def compatible(self, other):
        return compatible(self, other)
        #return conv_factor + dest
    #def simplify(self, string):
    def number(self): 
        '''return the number portion of the unit string'''
        return 'not yet implemented, sorry!'
    def unit(self):
        '''return the unit portion of the unit string'''
        return 'not yet implemented, sorry!'
    
class Process(yaml.YAMLObject):
    yaml_tag = '!process'
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "Process(%s)" % (self.name)
    

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
        assert self.form=="UN" and compatible(self.pitch, 'rev/inch'), "this only works for triangular threads atm"
        s = Template('($diameter)-0.6495919rev/($pitch)') #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(simplify(string)).to('in')
  
    def minor_diameter(self):
        assert self.form=="UN" and compatible(self.pitch, 'rev/inch'), "this only works for triangular threads atm"
        s = Template('($diameter)-1.299038rev/($pitch)')  #machinery's handbook 27ed page 1502
        string = s.safe_substitute(diameter=self.diameter, pitch=self.pitch)
        return Unit(simplify(string)).to('in')
    
    def clamping_force(self, torque, efficiency=0.1):
        s = Template('($torque)*($pitch)*$efficiency')
        string = s.safe_substitute(torque=torque, pitch=self.pitch, efficiency=efficiency) #fill in template keywords
        simplified = simplify(string) #compute the expression
        force = Unit(simplified).to('lbf') #I guess this looks better than kg*m/s^2, but there should be a default units setting somewhere
        return force
  
    def tensile_area(self):
        assert compatible(self.pitch, 'rev/inch')
        s = Template('pi/4*(($Dm+$Dp)/2)^2') #machinery's handbook 27ed page 1502 formula 9 "tensile-stress area of screw thread"
        string = s.safe_substitute(Dm=self.minor_diameter(), Dp=self.pitch_diameter())
        simplified = simplify(string)
        return Unit(simplified).to('in^2')
  #max torque requires finding the combined "von mises" stress, given on page 1498
  #because the screw body will twist off as a combination of tensile and torque shear loads

class Component(yaml.YAMLObject):
    interfaces = []
    #def __init__(self):
    #        pass
    pass

class Screw(Component):
    yaml_tag = "!screw"
    '''a screw by itself isn't a fastener, it needs a nut of some sort'''
    ##i suppose this stuff should go in a screws.yaml file or something, along with standard diameters
    proof_load = {#grade:load, proof load is defined as load bolt can withstand without permanent set
        '1':'33ksi',
        '2':'55ksi',
        '3':'85ksi',
        '5':'85ksi',
        '7':'105ksi',
        '8':'120ksi',
        }
    tensile_strength = {#grade:load, tensile strength is defined as load bolt can withstand without breaking
        '1':'60ksi',
        '2':'74ksi',
        '3':'110ksi',
        '5':'120ksi',
        '7':'133ksi',
        '8':'150ksi',
        }
    def __init__(self, thread, length, grade="2"):
        '''length is defined as the distance from bottom of the head for all screws but 
        flat head and set screws which use the top of the head instead'''
        #thread.__init__()
        self.thread, self.length, self.grade = thread, length, grade
        if self.thread.length is None: self.thread.length = self.length
        #note these tables vary from source to source; might want to check if it really matters to you
        
    def max_force(self):
        s = Template('$area*$strength')
        string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.proof_load[self.grade])
        simplified = simplify(string)
        return Unit(simplified).to('lbf')
  
    def breaking_force(self):
        s = Template('$area*$strength')
        string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.tensile_strength[self.grade])
        simplified = simplify(string)
        return Unit(simplified).to('lbf')

class Bolt(Fastener):
    '''a screw by itself cannot convert torque to force. a bolt is a screw with a nut'''
    def __init__(self, screw, nut):
        self.screw = screw
        self.nut = nut

def load(string):
    for cls in [Range]:#, Uncertainty]: #only one at a time works so far?
        assert hasattr(cls, 'yaml_pattern')
        if hasattr(cls, 'yaml_pattern'):
            yaml.add_constructor(cls.yaml_tag, lambda loader, node: cls.constructor(loader.construct_scalar(node)))
            yaml.add_implicit_resolver(cls.yaml_tag, re.compile(cls.yaml_pattern))
        
    return yaml.load(string)

def dump(value, filename=None):
    for cls in [Unit, Range]:
        assert hasattr(cls, 'yaml_repr')
        if hasattr(cls, 'yaml_repr'):
            repr = lambda dumper, instance: dumper.represent_scalar(instance.yaml_tag, instance.yaml_repr())
            yaml.add_representer(cls, repr )
    retval = yaml.dump(value, default_flow_style=False)
    if filename is not None:
        f = open(filename, 'w')
        f.write(retval)
    else:
        return retval
    #some stdout call here might not be a bad idea

def main():
    #basic self-test demo
    foo = load(open('tags.yaml'))
    print dump(foo)

if __name__ == "__main__":
    main()
