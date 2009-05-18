#skdb.py
#first go at a YAML file format, generated automatically from python classes
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os
from string import Template
#unum looks rather immature, perhaps I will write a wrapper for GNU units instead
#scientific.Physics.PhysicalQuantities looks ok-ish

class UnitError(Exception): pass 
class NaNError(Exception): pass


def simplify(string):
    rval = os.popen("units -t '" + string + "'").read().rstrip('\n')
    error = re.search('Unknown|Parse|Error', rval)
    if error:  
      raise UnitError, rval
    nan = re.search(' nan?!o', rval)
    if nan:
      raise NaNError, rval
#   -t flag takes care of this
#    if not rval.__contains__('Definition'):
#      raise UnitError, "unexpected problem with units program: " + rval
    for i in ['..']: #units bugs out on '1..2'
      if string.__contains__(i):
        print "Typo?"+ string + ": contains '" + i + "'"
    return rval

def compatible(a, b):
    '''check if both expressions boil down to the same base units'''
    try: simplify(str(a) + '+' + str(b))
    except UnitError: return None
    else: return True

class Measurement:
  '''try to preserve the original units, and provide a wrapper to the GNU units program'''
  def __init__(self, string, uncertainty=None):
    simplify(string) #check if we have a good unit format to begin with. is there a better way to do this?
    self.uncertainty = uncertainty
    e_number = '([+-]?\d*\.?\d*([eE][+-]?\d+)?)' #engineering notation
    #match = re.match(e_number + '?(\D*)$', string) #i dunno wtf i was trying to do here
    match = re.match(e_number + '?(.*)$', string)
    if match is None: raise UnitError, string
    try: self.number = float(match.group(1))
    except ValueError: self.number = 1.0
    self.unit = match.group(3)

  def __repr__(self):
    return str(self.number) + self.unit #ew
   
  def __mul__(self, other):
    if isinstance(other, Unit):
      return Measurement(str(self.number*other.number) + self.unit + '*' + other.unit)
    else:
      return Measurement(str(self.number * other) + self.unit)
  __rmul__ = __mul__

  def __div__(self, other):
    if isinstance(other, Measurement):
      return Measurement(str(self.number/other.number) + self.unit + '/' + other.unit)
    else:
      return Measurement(str(self.number / other) + self.unit)
  __rdiv__ = __div__
  
  def to(self, dest):
    conv_factor = os.popen("units -t '" + self.__repr__() + "' '" + dest + "'").read().rstrip('\n')
    return Measurement(conv_factor + dest)
#    return conv_factor + dest
#  def simplify(self, string):


mm = Measurement('1mm')

class Fastener:
  '''could be a rivet, could be a bolt. duct tape? superglue? twine? hose clamp?
  these methods are what actually get called by higher levels of abstraction'''
  def __init__(self, force, rigidity, safety_factor=7):
    pass


class Thread:
  '''examples: ballscrews, pipe threads, bolts - NOT any old helix'''
  def __init__(self, diameter, pitch, form="UN"):
    self.diameter, self.pitch, self.form = Measurement(diameter), Measurement(pitch), form
    
  def clamping_force(self, torque, efficiency=0.1):
    s = Template('($torque)*($pitch)*$efficiency')
    string = s.safe_substitute(torque=torque, pitch=self.pitch, efficiency=efficiency) #fill in template keywords
    simplified = simplify(string) #compute the expression
    force = Measurement(simplified).to('lbf') #I guess this looks better than kg*m/s^2, but there should be a default units setting somewhere
    return force
  
  def tensile_area(self):
      #machinery's handbook 26th edition page 1490 formula 2a "tensile-stress area of screw thread"
      assert compatible(self.pitch, 'rev/inch')
      s = Template('pi/4*($D-0.9743rev/($n))^2') #n is rev/inch
      string = s.safe_substitute(D=self.diameter, n=self.pitch)
      simplified = simplify(string)
      return Measurement(simplified).to('in^2')
  


class Screw(Fastener):
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
    #note these tables vary from source to source; might want to check if it really matters to you
  
  def max_force(self):
      s = Template('$area*$strength')
      string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.proof_load[self.grade])
      simplified = simplify(string)
      return Measurement(simplified).to('lbf')
  
  def breaking_force(self):
      s = Template('$area*$strength')
      string = s.safe_substitute(area=self.thread.tensile_area(), strength=Screw.tensile_strength[self.grade])
      simplified = simplify(string)
      return Measurement(simplified).to('lbf')
        
def main():
    screw = yaml.load(open('screw.yaml'))['screw']
    print yaml.dump(screw)
    print screw.thread.clamping_force('20N*m/rev')
    print screw.thread.clamping_force('100ft*lbf')
    print screw.thread.tensile_area()
    print screw.max_force()

if __name__ == "__main__":
  main()
