#!/usr/bin/python
'''
settings.py - load settings from config.yaml
environmental variables overwrite values from config.yaml

environmental variables:
    SKDB_PACKAGE_DIR = path to where packages are hoarded
'''
import os
import yaml

#this basically does "cd ../packages" from settings.py (__file__ is the path to settings.py)
sep = os.path.sep
path = os.path.realpath(__file__).split(sep)
path.pop()
path.pop()

#try loading values from config.yaml
path.append("config.yaml")
config_yaml_path = sep.join(path)
paths = yaml.load(open(config_yaml_path, "r"))

#base path to skdb installation
base_path = os.path.realpath(__file__).split(sep)
base_path.pop() #pop off "settings.py"
base_path.pop() #pop off "core"
base_path = sep.join(base_path)
assert os.path.isabs(base_path), "base_path must be an absolute path" #shouldn't happen

new_paths = {}
#assume all relative paths refer to skdb/ (not skdb/core/)
for key in paths:
    path = paths[key]
    if type(path) == str:
        #if the path is relative (not absolute)
        if not os.path.isabs(path):
            #convert from relative path to absolute path
            new_path = os.path.join(base_path, path)
            new_paths[key] = new_path
        else: new_paths[key] = path
    else: new_paths[key] = path
paths = new_paths

#legacy
paths["SKDB_PACKAGE_DIR"] = paths["package dir"]
paths["SKDB_PACKAGE_REPO"] = paths["repositories"][0]
conversion_table = {
    "SKDB_PACKAGE_DIR": "package dir",
    "SKDB_PACKAGE_REPO": "repositories", #sorta
}
#respect environmental variables (they aren't necessary)
#TODO: phase out
for named_variable in paths:
    if os.environ.has_key(named_variable):
        paths[named_variable] = os.environ[named_variable]
        #set the "new" settings variable to the value of the environmental variable
        if named_variable in conversion_table: paths[conversion_table[named_variable]] = os.environ[named_variable]

def package_path(package_name):
    '''returns the full package path'''
    return os.path.join(paths["package dir"],package_name)
