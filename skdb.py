#skdb.py
#first go at a YAML file format, generated automatically from python classes
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os

#unum looks rather immature, perhaps I will write a wrapper for GNU units instead
#scientific.Physics.PhysicalQuantities looks ok-ish

extract_number = re.compile("\W+")

def check_units(string):
#  for i in ['++', '--', '//', '**', '&', '#', '@', '!', '<', '>', ',', '=', '_', '..']:
  for i in ['..']: #units bugs out on '1..2'
    if string.__contains__(i): raise "UnitError", string + ": contains '" + i + "'"
  rval = os.popen("units -tv '" + string + "'").read()
  error = re.search('Unknown|Parse|Error| nan ', rval)
  if error: raise "UnitError", rval
  if not rval.__contains__('Definition'):
      raise "UnitError", "unknown problem with units program: " + rval
  return rval.rstrip('\n')

class Unit:
  '''i wonder if i should try to preserve the native units'''
  def __init__(self, string):
    check_units(string)
    e_number = '([+-]?\d*\.?\d*([eE][+-]?\d+)?)'
    match = re.match(e_number + '?(\D*)', string)
    if match is None: raise "UnitError", string
    try: self.number = float(match.group(1))
    except ValueError: self.number = 1.0
    self.unit = match.group(3)

  def __repr__(self):
    return str(self.number) + self.unit #ew
   
  def __mul__(self, other):
    if isinstance(other, Unit):
      return Unit(str(self.number*other.number) + self.unit + '*' + other.unit)
    else:
      return Unit(str(self.number * other) + self.unit)
  __rmul__ = __mul__

  def __div__(self, other):
    if isinstance(other, Unit):
      return Unit(str(self.number/other.number) + self.unit + '/' + other.unit)
    else:
      return Unit(str(self.number / other) + self.unit)
  __rdiv__ = __div__
  
  def to(self, dest):
    conv_factor = os.popen("units -t '" + self.__repr__() + "' '" + dest + "'").read().rstrip('\n')
    return Unit(conv_factor + dest)
#    return conv_factor + dest

mm = Unit('1mm')
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

