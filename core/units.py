from yamlcrap import FennObject
import re, os
from string import Template

combined_dat_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'combined.dat')

if not os.access(os.path.join(os.path.dirname(os.path.realpath(__file__)), "combined.dat"), os.F_OK):
    #build the new db for our custom units
    f1 = open('/usr/share/misc/units.dat').read()
    current_path = os.path.dirname(os.path.realpath(__file__))
    f2 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'supplemental_units.dat')).read()
    f3 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'combined.dat'), 'w')
    f3.write(f1+f2)
    f3.close()

#unum looks rather immature, perhaps I will write a wrapper for GNU units instead
#scientific.Physics.PhysicalQuantities looks ok-ish        
class UnitError(Exception): pass 
class NaNError(Exception): pass

class Unit(FennObject):
    sci = '([+-]?\d*.?\d+([eE][+-]?\d+)?)' #exp group leaves turds.. better way to do regex without parens?
    yaml_tag = "!unit"
    '''try to preserve the original units, and provide a wrapper to the GNU units program'''
    units_call = "units -f %s -t " % (combined_dat_path) #export LOCALE=en_US; ?
    def __init__(self, string=None):
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
        #so we can play nice with the 'quantities' package:
        if hasattr(string, "units"): string = string.units.dimensionality.string
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

class Range(FennObject):
    yaml_tag = "!range"
    sci =Unit.sci
    #expression should look something like: 1e4 m .. 2km
    yaml_pattern = sci+'\s*(\D?.*)?\s*\.\.\s*'+sci+'\s*(\D?.*)$'
    def __init__(self, min=None, max=None):
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

class Uncertainty(Range):
    '''predicted or observed range of error in the measurement'''
    yaml_tag = "!uncertainty" #ehh.. going to do something with this eventually
    sci =Unit.sci
    yaml_pattern = '^\+-' + sci + '\s*(\D?.*)$' #+-, number, units
    #TODO from_yaml method using existing __init__
    #TODO args should be (min, max), assert isinstance Unit
    def __init__(self, string=None):
        match = re.match('^\+-(.*)', string)
        if match: unit = match.group(1)
        else: raise SyntaxError, "'"+ string +"'" + ": uncertainty must begin with +-, for now at least" #got any better ideas?
        Unit.__init__(self, unit)
    def __repr__(self):
        return 'Uncertainty('+ Unit.__repr__(self) +')'
    def yaml_repr(self):
        return "+-%s" % (self.string)

