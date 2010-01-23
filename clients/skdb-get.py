#!/usr/bin/python
"""
skdb-get.py - "apt-get for real stuff"

run: python skdb-get.py screw

please see ../config.yaml to tell skdb where packages are stored
"""
import sys, os
import getpass
from string import join
import skdb
from skdb import settings

#for parsing command line arguments
from skdb.thirdparty import optfunc

def get_package(package_name, verbose=False, repo=settings.paths["repositories"], package_dir=skdb.settings.paths["package_dir"], branch="master", *args, **keywords):
    '''usage: %prog <package name> [--verbose] [--repo <URL>] [--package-dir /usr/local/share/skdb/] [--branch master]
    download hardware and exit'''
    #assert not have_package(package_name), "package already installed"
    if package_name == "help" or package_name == "": print get_package.__doc__ #how do i do this?

    if not isinstance(repo, list): repo = [repo] #it's actually a list in the config file
    if repo[0][-1:] != "/": repo[0] = repo[0]+"/" #add trailing slash to url if not there
    package_url = repo[0] + package_name + "/.git"

    #make package_dir exist
    os.system('mkdir -p "%s"' % (package_dir)) #package names cant have spaces so why the quotes?
    
    subdir = os.path.join(package_dir, package_name)
    if os.path.exists(subdir):
        command = 'cd "%s"; git pull origin "%s"' % (subdir, branch)
        print "updating:", package_name
    else: 
        command = 'cd "%s"; git clone "%s"' % (package_dir, package_url)
        print "installing:", package_name
    if verbose: print "command is: ", command
    exit_status = os.system(command)
    if exit_status != 0: raise EnvironmentError, "something went wrong at "+ package_url
    if verbose: print "checking %s for dependencies..." % (package_name)
        
    return

if __name__ == '__main__':
    optfunc.run(get_package)
