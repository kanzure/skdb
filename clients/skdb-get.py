#!/usr/bin/python
"""
skdb-get.py - "apt-get for real stuff"

environmental variables:
    - SKDB_PACKAGE_PATH
"""
__version__ = "0.0.1"

import sys, os
from skdb import settings

#for parsing command line arguments
from skdb.core import optfunc

def get_package(package_name, verbose=False, repo=settings.paths["SKDB_PACKAGE_REPO"], package_dir=settings.paths["SKDB_PACKAGE_DIR"], **kwarg):
    '''Usage: %prog <package name> [--verbose] [--repo http://adl.serveftp.org/skdb-packages/] [--package-dir /usr/share/skdb-packages]
    download hardware and exit'''
    if have_package(package_name):
        print "package already installed"
    print "getting package: ", package_name
    package_url = repo + "/" + package_name + ".git"
    #this is kinda custom for the moment
    os.system("cd %s; git clone %s;" % (package_dir, package_url))
    return

if __name__ == '__main__':
    optfunc.run(get_package)

