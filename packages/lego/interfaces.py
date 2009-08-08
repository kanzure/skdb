#!/usr/bin/python
'''this file more or less describes the grammar used for constructing things out of Lego
not done. see http://mr-bucket.co.uk/GLIDE/LCD_File_Format.html#Implimentation
for part examples see http://guide.lugnet.com/partsref/search.cgi?q=XXXX
or http://img.lugnet.com/ld/XXXX.gif
'''
from skdb import Interface

class Joint:
    '''should pull in some kinematics from elsewhere; PyODE?'''
    pass

class SphericalJoint(Joint): pass

class PlanarJoint(Joint): pass

class RevoluteJoint(Joint): pass

class PrismaticJoint(Joint): pass

class GearJoint(Joint): pass


class Discrete:
    '''allows only a certain set of values'''
    pass

grammar = {
    'Stud':{'complement':['AntiStud', 'Stud'], 'example':'3005'}}

class Feature(Interface):
    yaml_tag='!lego_feature'
    def __repr__(self):
        try: part_name = self.part.name
        except AttributeError: part_name = None
        
        try: name = self.name
        except AttributeError: name = None
        
        return "%s(part=%s,name=%s)" % (self.__class__.__name__, part_name, name)

class PressFit(Feature):
    '''this should probably link up with some other class'''
    pass

class SnapFit(Feature):
    '''same as PressFit but with less friction, and a restorative force'''
    pass

class Hinge(RevoluteJoint, SnapFit): pass

