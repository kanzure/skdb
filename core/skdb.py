#skdb.py
#(c) ben lipkowitz 11/16/08, distributed under the GPL version 2 or later

import yaml
import re
import os
import sys
from string import Template as string_template
from template import Template

from units import Unit, Range, Uncertainty, UnitError, NaNError
from interface import Interface, Connection
from part import Part
from yamlcrap import FennObject, Dummy, tag_hack
#from threads import Thread
import settings

debug = False

# the following aren't our responsibility, actually (pythonOCC?)
#class Circle(yaml.YAMLObject)
#class Cylinder(yaml.YAMLObject)
#class InterfaceGeom(yaml.YAMLObject):

def prettyfloat(num):                                                                                      
    '''round down to 0 if abs(num) < +-1e-13, gets rid of icky floating point errors'''              
    return str(float("%.13f" % (float(num))))     

def check_unix_name(name):
    '''returns True if name (string) is a valid unix_name'''
    assert name, "name is empty"
    check = re.match('^[a-zA-Z0-9_\-.]*$', name)
    assert check, 'allowed characters in a name are: a-z, 0-9, "-", ".", and "_". Instead, got: "'+str(name)+'"'
    if check: return True
    else: return False

def package_file(package, filename, mode='r'):
    '''construct a dummy package and return a filehandler for filename.
    needed for packages to find their own files (can't be used as a method of Package)'''
    dummy = Package(package)
    package_path = dummy.path()
    filepath = os.path.join(package_path, filename)
    try: #fail early
        assert os.access(filepath, os.F_OK)
        return open(filepath, mode)
    except AssertionError: 
        raise IOError, 'error in package "'+package+'": could not read file "'+filename+'"'


def open_package(path):
    '''just a synonym for load_package'''
    return load_package(path)

def load_package(name):
    '''returns a package loaded from the filesystem
    input should be something like "f-16" or "human-exoskeleton-1.0"
    see settings.paths['SKDB_PACKAGES_DIR']'''
    if not check_unix_name(name): #fail even if asserts are turned off
        return None
    assert hasattr(settings,"paths")
    assert settings.paths.has_key("SKDB_PACKAGE_DIR")
    package_path = os.path.join(settings.paths["SKDB_PACKAGE_DIR"],name)
    assert os.access(settings.paths['SKDB_PACKAGE_DIR'], os.F_OK), str(package_path)+": skdb package not found or unreadable"
    #must have the required files
    required_files = ["metadata.yaml", "data.yaml"]
    for file in required_files:
        package_file(name, file)
        #assert os.access(os.path.join(package_path, file), os.F_OK), str(package_path)+": "+file+" not found or unreadable"
    loaded_package = load(package_file(name, 'metadata.yaml'))
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

class Package(FennObject): #should this be a FennObject? ideally it should spit out metadata.yaml, data.yaml, etc.
    yaml_tag='!package'
    def __init__(self, name=None, license=None, urls=None, modules=None):
        self.name = name
        self.license = license
        self.urls = urls
    def post_init_hook(self):
        '''yaml calls this after loading a package'''
        check_unix_name(self.name)
    def path(self):
        '''returns the absolute path on the file system to the package folder'''
        check_unix_name(self.name)
        return settings.package_path(self.name)
    def load_data(self, file=None):
        '''loads all the files listed in "source data:" from metadata.yaml'''
        if not file:
            catalog = getattr(self, 'source data')
        else: catalog = [file]
        for x in catalog:
            self.overlay(load(package_file(self.name, x))) #merge data from entire catalog into package
            return self
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
        assert self.name is not None, "package name"
        assert self.functionality is not None, "functionality"
        assert self.created is not None, "created"
        assert self.updated is not None, "updated"
        assert self.version is not None, "version"
        assert self.description is not None, "description"
        assert self.classes is not None, "classes"
        assert self.source_data is not None, "source data"
        assert self.dependencies is not None, "dependencies" #unless you really know what you're doing?
        return True
    
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
    load_package('screw')
    package = load(open('tags.yaml'))
    print dump(package)

if __name__ == "__main__":
    main()
