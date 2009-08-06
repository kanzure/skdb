#!/usr/bin/python
'''
settings.py - end-user settings for skdb

environmental variables:
    SKDB_PACKAGE_DIR = path to where packages are hoarded
'''
import os

try:
    SKDB_PACKAGE_DIR = os.environ["SKDB_PACKAGE_DIR"]
except KeyError, err:
    #this basically does "cd ../packages" from settings.py (__file__ is the path to settings.py)
    sep = os.path.sep
    path = os.path.realpath(__file__).split(sep)
    path.pop()
    path.pop()
    path.append('packages/')
    SKDB_PACKAGE_DIR = sep.join(path)

paths = {
        'SKDB_PACKAGE_DIR': SKDB_PACKAGE_DIR,
        }

def package_path(package_name):
    '''returns the full package path'''
    return os.path.join(SKDB_PACKAGE_DIR,package_name)
