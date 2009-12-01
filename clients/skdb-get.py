#!/usr/bin/python
"""
skdb-get.py - "apt-get for real stuff"

run: sudo python skdb-get.py screw

please see ../config.yaml
"""
import sys, os
import getpass
from string import join

if not getpass.getuser() == "root":
    print "you must be root"
    exit(0)
if not os.path.abspath(__file__).count("clients")>0:
    print "you must run this from the clients/ directory"
    exit(0)

#root user probably doesn't know wtf skdb is
#update $PYTHONPATH to point to skdb
dir_location = os.path.abspath(__file__)
print "dir_location is: ", dir_location
dir_location = dir_location.split("/") #make it a list
dir_location.pop() #remove "skdb-get.py"
dir_location.pop() #remove "clients"
dir_location.pop() #remove skdb folder
print "dir_location is: ", dir_location
dir_location = join(dir_location, "/")
sys.path.append(dir_location) #add it to the python path

import skdb
from skdb import settings

#for parsing command line arguments
from skdb.thirdparty import optfunc

def get_package(package_name, verbose=False, repo=settings.paths["SKDB_PACKAGE_REPO"], package_dir=skdb.settings.path, **keywords):
    '''usage: %prog <package name> [--verbose] [--repo http://adl.serveftp.org/skdb-packages/] [--package-dir /usr/local/share/skdb/]
    download hardware and exit'''
    #assert not have_package(package_name), "package already installed"
    
    print "getting package: ", package_name
    package_url = repo + "/" + package_name + "/.git"

    #make package_dir exist
    os.system("mkdir -p \"%s\"" % (package_dir))

    #this is kinda custom for the moment
    command = "cd \"%s\"; git clone \"%s\";" % (package_dir, package_url)
    print "command is: ", command
    os.system(command)
    return

if __name__ == '__main__':
    optfunc.run(get_package)
