#skdb.py
#first go at a YAML file format, generated automatically from python classes
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os

#unum looks rather immature, perhaps I will write a wrapper for GNU units instead
#scientific.Physics.PhysicalQuantities looks ok-ish

class UnitError(Exception): pass 
class NaNError(Exception): pass

class Measurement:
  '''try to preserve the original units, and provide a wrapper to the GNU units program'''
  def __init__(self, string, uncertainty=None):
    self.check(string=string)
    self.uncertainty = uncertainty
    e_number = '([+-]?\d*\.?\d*([eE][+-]?\d+)?)' #engineering notation
    match = re.match(e_number + '?(\D*)$', string)
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

  def check(self, string=None):
    if string is None:
      string = self.__repr__()
    rval = os.popen("units -t '" + string + "'").read().rstrip('\n')
    error = re.search('Unknown|Parse|Error', rval)
    if error:  
      raise UnitError, rval
    nan = re.search(' nan?!o', rval)
    if nan:
      raise NaNError, rval
#    if not rval.__contains__('Definition'):
#      raise UnitError, "unexpected problem with units program: " + rval
    for i in ['..']: #units bugs out on '1..2'
      if string.__contains__(i):
        print "Typo?"+ string + ": contains '" + i + "'"
    return rval

  def compatible(self, b):
    '''check if both expressions boil down to the same base units'''
    try: Measurement(str(self) + '+' + str(b)).check()
    except UnitError: return None
    else: return True



mm = Measurement('1mm')
#inch = mm*25.4
#print yaml.dump(inch)

class Thread:
  def __init__(self, diameter, pitch, form="UN"):
    self.diameter, self.pitch, self.form = diameter, pitch, form

class Screw:
  def __init__(self, thread, length, grade="3"):
    '''length is defined as the distance from bottom of the head for all screws but 
    flat head and set screws which use the top of the head instead'''
    thread.__init__()

