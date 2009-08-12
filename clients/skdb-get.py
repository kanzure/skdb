#!/usr/bin/python
"""
skdb-get.py - "apt-get for real stuff"

environmental variables:
    - SKDB_PACKAGE_PATH
"""
import sys
from skdb import settings
import cmdsyntax

__version__ = "0.0.1"

if __name__ == '__main__':
    syntax = "<command> <option>"
    syntax_obj = cmdsyntax.Syntax(syntax)
    matches = syntax_obj.get_args(sys.args[1:])
    
    if len(matches) != 1:
        sys.stderr.write("Usage: %s %s\n\n" % (sys.argv[0], syntax))
        sys.stderr.write("skdb-get.py (version %s)" % (__version__))
        sys.stderr.write("usage information goes here")
        sys.exit(1)

#other stuff happens here

