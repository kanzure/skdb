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
    #err.message is "SKDB_PACKAGE_DIR"
    #hacker's setting: ../packages/
    basename = os.path.basename(__file__)
    realpath = os.path.realpath(__file__)
    current_filename_len = len(os.path.basename(realpath))
    folder = realpath[:-current_filename_len]
    current_foldername_len = len(os.path.basename(os.path.dirname(folder)))
    parentfolder = folder[:-current_foldername_len - len(os.path.sep)]
    SKDB_PACKAGE_DIR = os.path.join(parentfolder,"packages")

paths = {
        'SKDB_PACKAGE_DIR': SKDB_PACKAGE_DIR,
        }
