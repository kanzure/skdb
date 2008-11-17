#skdb.py
#first go at a YAML file format, generated automatically from python classes
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml


#unum looks rather immature, perhaps I will write a wrapper for GNU units instead

class Unit():
  '''i'm sure this will fill up with some funky stuff soon enough'''
  def __init__(self, number, unit):
    self.number = number
    self.unit = unit

  def __repr__():
    return self.number + self.unit #ew
   
  def __mul__(self, other):
    if isinstance(other, Unit):
      return Unit(self.number * other.number, self.unit + '*' + other.unit)
    else:
      return Unit(self.number * other, self.unit)
  __rmul__ = __mul__

def to(dest):
    return os.system('units ' + self.__repr__ + ' ' + dest)

mm = Unit(1, 'mm')
inch = mm*25.4
print yaml.dump(inch)

class Thread:
  def __init__(self, diameter, pitch, form="UN"):
    self.diameter, self.pitch, self.form = diameter, pitch, form

class Screw:
  def __init__(self, thread, length, grade="3"):
    '''length is defined as the distance from bottom of the head for all screws but 
    flat head and set screws which use the top of the head instead'''
    thread.__init__()

