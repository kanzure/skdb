#skdb.py
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os
import sys
from string import Template as string_template
from template import Template

from units import Unit, Range, Uncertainty, UnitError, NaNError
from interface import Interface, Connection, Mate
from part import Part
from yamlcrap import FennObject, Dummy, tag_hack
from threads import Thread
import settings

debug = False

# the following aren't our responsibility, actually (pythonOCC?)
#class Circle(yaml.YAMLObject)
#class Cylinder(yaml.YAMLObject)
#class InterfaceGeom(yaml.YAMLObject):

def check_unix_name(name):
    '''returns True if name (string) is a valid unix_name
    allowed characters in a unix_name are: a-z, 0-9, - and _'''
    return name.isalpha()

def open_package(path):
    '''just a synonym for load_package'''
    return load_package(path)

def load_package(path):
    '''returns a package loaded from the filesystem
    see settings.paths['SKDB_PACKAGES_DIR'] btw'''
    if path == None:
        return None
    assert check_unix_name(path)
    assert hasattr(settings,"paths")
    assert settings.paths.has_key("SKDB_PACKAGE_DIR")
    package_path = os.path.join(settings.paths["SKDB_PACKAGE_DIR"],path)
    assert os.access(settings.paths['SKDB_PACKAGE_DIR'], os.F_OK), str(package_path)+": skdb package not found or unreadable"
    #must have the required files
    required_files = ["metadata.yaml", "data.yaml"]
    for file in required_files:
        assert os.access(os.path.join(package_path, file), os.F_OK), str(package_path)+": "+file+" not found or unreadable"
    loaded_package = load(open(os.path.join(package_path, "metadata.yaml")))
    import_package_classes(loaded_package, package_path)
    return loaded_package
    
def import_package_classes(loaded_package, package_path):
    '''assigns classes to the Package's namespace; for example:
    package = load_package('lego')
    mybrick = package.Brick()'''
    for module_name in loaded_package.classes.keys():
        try: 
            module = __import__(module_name)
        except ImportError:
            sys.path.append(package_path)
            module = __import__(module_name)
        for class_name in loaded_package.classes[module_name]:
            cls = getattr(module, class_name)
            setattr(loaded_package, class_name, cls )
            setattr(cls, "package", loaded_package)


class Package(FennObject):
    yaml_tag='!package'
    def __init__(self, name=None, unix_name=None, license=None, urls=None, modules=None):
        self.name, self.unix_name, self.license = None, None, None
        return
        self.name = name
        self.unix_name = unix_name
        if unix_name == None:
            self.unix_name = name
            assert check_unix_name(self.unix_name)
        self.license = license
        self.urls = urls
    def post_init_hook(self):
        '''yaml calls this after loading a package'''
        #need to set a unix name
        if not self.unix_name:
            if self.name: self.unix_name = self.name
        return
    def path(self):
        '''returns the absolute path on the file system to the package folder'''
        assert hasattr(self, "unix_name"), "this package must have a unix_name attribute-- was post_init_hook called?"
        return settings.package_path(self.unix_name)
    def load(self, content, only_classes=None):
        '''loads some yaml (not necessarily into type Package)
        it's kind of fishy since a package is multiple files at the moment.'''
        returns = yaml.load(content)
        if not only_classes == None:
            #only return the objects that are of type only_classes
            #FIXME: allow "only_classes" to be a list
            real_returns = []
            for (k,v) in returns.items():
                if str(type(v)) == only_classes: #there has to be a better way to do this
                    #set the name attribute to the keyname
                    v.name = k
                    real_returns.append(v)
            return real_returns
        return returns
    def dump(self):
        '''returns this object in yaml'''
        return yaml.dump(self)
    def dump_metadata(self):
        '''dump only the content for or from metadata.yaml'''
        raise NotImplementedError
    def dump_template(self):
        '''dump only the content for or from template.yaml'''
        raise NotImplementedError
    def dump_data(self):
        '''dump only the content for or from data.yaml'''
        raise NotImplementedError
    def makes_sense(self):
        '''checks for whether or not the package data makes sense'''
        raise NotImplementedError

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
    def __init__(self, depends=None, parameter=None): #i dont like 'depends' but cant think of a better word
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
    
class Process(FennObject):
    yaml_tag = '!process'
    def __init__(self, name=None):
        self.name, self.classification, self.mechanism, self.geometry, self.surface_finish, self.consumables, self.functionality, self.effects, self.parameters, self.safety = None, None, None, None, None, None, None, None, None, None
        self.name = name

    #def __repr__(self):
        #return "Process(%s)" % (self.name)
    

class Material(Package):
    yaml_tag = '!material'
    def __init__(self, name=None, density=1, specific_heat=1, etc=None): #TODO figure out what goes here
        self.name = name
        self.density = density
        self.specific_heat = specific_heat

class Fastener(Package):
    yaml_tag = '!fastener'
    '''could be a rivet, could be a bolt. duct tape? superglue? twine? hose clamp?
    these methods are what actually get called by higher levels of abstraction'''
    def __init__(self, force=None, rigidity=None, safety_factor=7):
        pass

class Component(yaml.YAMLObject):
    '''is this sufficiently generic or what?'''
    yaml_tag = '!component'
    interfaces = []
    #def __init__(self):
    #        pass
    pass

class Bolt(Fastener):
    '''a screw by itself cannot convert torque to force. a bolt is a screw with a nut'''
    def __init__(self, screw=None, nut=None):
        self.screw = screw
        self.nut = nut

implicit_resolved=[]
def load(string):
    global implicit_resolved
    for cls in [Range, RuntimeSwitch, Formula, Uncertainty]: #only one at a time works so far?
        if hasattr(cls, 'yaml_pattern') and cls not in implicit_resolved:
            yaml.add_implicit_resolver(cls.yaml_tag, re.compile(cls.yaml_pattern))
            implicit_resolved.append(cls)
    tmp = yaml.load_all(string)
    rval = tmp.next() #this might be tag_hack
    if type(rval) == tag_hack:
        other_return_value = tmp.next() #a document listing which tags to ignore comes before the real metadata
        #now remove the tag_hack tags from the system
        for tag in rval.tags:
            rval.undo_tag_hack_for_tag(tag)
        return other_return_value
    else: return rval

def dump(value, filename=None):
    retval = yaml.dump(value, default_flow_style=False)
    if filename is not None:
        f = open(filename, 'w')
        f.write(retval)
    else:
        return retval
    #some stdout call here might not be a bad idea

def main():
    #basic self-test demo
    package = load(open('tags.yaml'))
    print dump(package)

if __name__ == "__main__":
    main()
