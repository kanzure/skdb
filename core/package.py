import settings
from yamlcrap import FennObject, load, yaml
import re, os, sys
from copy import copy, deepcopy

def check_unix_name(name):
    '''returns True if name (string) is a valid unix_name'''
    assert name, "check_unix_name: name is empty (name=\"%s\")" % (name)
    check = re.match('^[a-zA-Z0-9_\-.]*$', name)
    assert check, 'allowed characters in a name are: a-z, 0-9, "-", ".", and "_". Instead, got: "'+str(name)+'"'
    if check: return True
    else: return False

def package_file(package_name, filename, mode='r'):
    '''construct a dummy package and return a filehandler for filename.
    needed for packages to find their own files (can't be used as a method of Package)'''
    package_path = os.path.join(settings.paths["SKDB_PACKAGE_DIR"], package_name)
    filepath = os.path.join(package_path, filename)
    try: #fail early
        assert os.access(filepath, os.F_OK)
        return open(filepath, mode)
    except AssertionError: 
        raise IOError, 'error in package "'+package_name+'": could not read file "'+filename+'"'

def open_package(path):
    '''just a synonym for load_package'''
    return load_package(path)

def __lame_asserts__():
    assert hasattr(settings,"paths")
    assert settings.paths.has_key("SKDB_PACKAGE_DIR")

def load_metadata(name):
    '''returns a package loaded from the filesystem
    input should be something like "f-16" or "human-exoskeleton-1.0"
    this only loads the metadata and is safe if you haven't actually downloaded the entire package'''
    if not check_unix_name(name):
        return None
    __lame_asserts__()
    assert os.access(settings.paths['SKDB_PACKAGE_DIR'], os.F_OK), str(package_path)+": skdb package not found or unreadable"
    #must have the required files
    assert package_file(name, "metadata.yaml")
    loaded_package = load(package_file(name, "metadata.yaml"))
    return loaded_package

def load_package(name):
    '''returns a package loaded from the filesystem
    input should be something like "f-16" or "human-exoskeleton-1.0"
    see settings.paths['SKDB_PACKAGES_DIR']'''
    if not check_unix_name(name): #fail even if asserts are turned off
        return None
    __lame_asserts__()
    package_path = os.path.join(settings.paths["SKDB_PACKAGE_DIR"],name)
    assert os.access(settings.paths['SKDB_PACKAGE_DIR'], os.F_OK), str(package_path)+": skdb package not found or unreadable"
    #must have the required files
    required_files = ["metadata.yaml", "data.yaml"]
    for file in required_files:
        assert package_file(name, file) #just check if present
    loaded_package = load(package_file(name, 'metadata.yaml'))
    loaded_package.package_path = package_path
    loaded_package.import_package_classes()
    #import_package_classes(loaded_package, package_path)
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
    def __init__(self, name=None, data=True, create=True):
        '''name is name of the package
        data is True or False for whether or not to load the source data'''
        print "skdb.Package.__init__ -- name is: %s" % (name)
        if not hasattr(self, "name") and name is None: return #not like we can do much of anything
        if hasattr(self, "name") and name is None: self.name = name
        if not hasattr(self, "name") and name is not None: self.name = name
        if self.name is None: return #not like we can do much of anything
        #check if the package already exists
        filepath = self.path()
        pkg_exists = os.access(filepath, os.F_OK)
        if pkg_exists:
            #load it from a file
            pkg = deepcopy(Package.__load_package__(name, data=data))
            #put the values in the local dictionary
            for key in pkg.__dict__.keys():
                value = pkg.__dict__[key]
                self.__dict__[key] = deepcopy(value)
            self.post_init_hook(data=data) #this isn't yaml so we have to call the hook on our own
        elif create==False: raise ValueError, "no package by that name"
    def post_init_hook(self, data=True):
        '''FennObject.from_yaml calls this 'after' loading a package'''
        check_unix_name(self.name)
        if data and hasattr(self, "source data"):
            self.load_data()
    @staticmethod
    def __load_package__(package_name, data=True):
        '''loads a package. call the constructor instead.'''
        __lame_asserts__()
        package_path = os.path.join(settings.paths["SKDB_PACKAGE_DIR"],package_name)
        assert os.access(settings.paths['SKDB_PACKAGE_DIR'], os.F_OK), str(package_path)+": skdb package not found or unreadable"
        #must have the required files
        required_files = ["metadata.yaml"]
        if data: required_files.append("data.yaml")
        for file in required_files:
            assert os.access(os.path.join(settings.package_path(package_name), file), os.F_OK) #check if present
        loaded_package = load(open(os.path.join(settings.package_path(package_name), "metadata.yaml"),"r"))
        loaded_package.package_path = package_path
        loaded_package.import_package_classes()
        if data: loaded_package.load_data()
        return loaded_package
    def import_package_classes(self):
        '''assigns classes to the Package's namespace; for example:
        package = Package("lego")
        mybrick = package.Lego()'''
        package_path = self.path()
        for module_name in self.classes.keys():
            try: 
                module = __import__(module_name)
            except ImportError:
                sys.path.append(package_path)
                module = __import__(module_name)
            for class_name in self.classes[module_name]:
                cls = getattr(module, class_name)
                setattr(self, class_name, cls )
                setattr(cls, "package", self)
    def path(self,package_name=None):
        '''returns the absolute path on the file system to the package folder'''
        if not hasattr(self, "name"): self.name = package_name
        elif self.name is None and package_name is not None: self.name = package_name
        check_unix_name(self.name)
        return settings.package_path(self.name)
    #def load_metdata(self, file=None):
    #'''loads metadata based off of the package name from the skdb package directory on localhost'''
    def load_data(self, file=None):
        '''loads all the files listed in "source data:" from metadata.yaml'''
        if not file:
            catalog = getattr(self, 'source data')
        else: catalog = [file]
        for x in catalog:
            self.overlay(load(open(os.path.join(self.path(), x)))) #merge data from entire catalog into package
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
    def makes_sense(self): #FIXME this is really lame
        '''checks for whether or not the package data makes sense'''
        assert self.name is not None, "package name"
        assert self.functionality is not None, "functionality"
        assert self.created is not None, "created"
        assert self.version is not None, "version"
        assert self.description is not None, "description"
        assert self.classes is not None, "classes"
        assert getattr(self, 'source data') is not None, "source data"
        assert self.dependencies is not None, "dependencies" #unless you really know what you're doing?
        return True

