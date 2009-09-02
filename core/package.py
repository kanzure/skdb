import settings
from yamlcrap import FennObject, load
import re, os, sys


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
        assert package_file(name, file) #just check if present
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
    def makes_sense(self): #FIXME this is really lame
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