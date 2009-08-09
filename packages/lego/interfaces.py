#!/usr/bin/python
'''this file more or less describes the grammar used for constructing things out of Lego
not done. see http://mr-bucket.co.uk/GLIDE/LCD_File_Format.html#Implimentation
for part examples see http://guide.lugnet.com/partsref/search.cgi?q=XXXX
or http://img.lugnet.com/ld/XXXX.gif
'''
import os
import skdb

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

#class Grammar(skdb.FennObject, dict):
#    yaml_tag='!lego_grammar'

fh = skdb.package_file('lego', 'grammar.yaml')
grammar = skdb.load(fh)['features']

#stuff values
for key in grammar.keys():
    grammar[key]['name'] = key

def dump_grammar_file():
    '''you probably should pipe through 'grep -v name'''''
    import yaml
    return yaml.dump(grammar)
    
class Feature(skdb.Interface):
    yaml_tag='!lego_feature'
    yaml_flow_style=False
    def __init__(self, name=None, type=None, part=None):
        skdb.Interface.__init__(self, name=name, part=part)
        self.type=type
    def post_init_hook(self):
        try:
            type = self.type
            self.overlay(grammar[type])
        except AttributeError: self.type = None
        
        try: part_name = self.part.name
        except AttributeError: part_name = None
        
        try: name = self.name
        except AttributeError: name = None
    def compatible(self, other):
        if other.type in self.complement:
            assert self.type in other.complement, 'vice versa not fulfilled for "%s" and "%s"' %(self.type, other.type)
            return True
        else: return False
        
    def __repr__(self):
        return "%s(part=%s,name=%s, type=%s)" % (self.__class__.__name__, self.part_name, self.name, self.type)
        
    def example_picture(self):
        '''example should be an ldraw number'''
        return "http://img.lugnet.com/ld/"+self.example+".gif"
        
    def example_lugnet(self):
        return "http://guide.lugnet.com/partsref/search.cgi?q="+self.example
        
    def example_peeron(self):
        return "http://www.peeron.com/inv/parts/"+self.example

class PressFit(Feature):
    '''this should probably link up with some other class'''
    pass

class SnapFit(Feature):
    '''same as PressFit but with less friction, and a restorative force'''
    pass

class Hinge(RevoluteJoint, SnapFit): pass

if __name__ == '__main__':
    print dump_grammar_file()