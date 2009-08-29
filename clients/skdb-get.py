#!/usr/bin/python
"""
skdb-get.py - "apt-get for real stuff"

environmental variables:
    - SKDB_PACKAGE_PATH
"""
__version__ = "0.0.1"

import sys
from skdb import settings

#for parsing command line arguments
from skdb.core import optfunc

def get_package(package_name, verbose=False, repo=settings.SKDB_PACKAGE_DIR):
    '''Usage: %prog <package name> [--verbose] [--repo http://adl.serveftp.org/skdb-packages/]
    download hardware and exit'''
    print "getting package: ", package_name
    return

if __name__ == '__main__':
    optfunc.run(get_package)

