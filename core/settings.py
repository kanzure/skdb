#!/usr/bin/python
'''
settings.py - load settings from config.yaml
environmental variables are ignored
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

#assume all relative paths refer to skdb/ (not skdb/core/)
for key in paths:
    if type(paths[key]) == str:
        paths[key] = os.path.normpath(os.path.expanduser(paths[key]))
        assert os.path.isabs(paths[key])

def package_path(package_name):
    '''returns the full package path'''
    return os.path.join(paths["package_dir"],package_name)
