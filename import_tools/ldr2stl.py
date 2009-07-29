#!/usr/bin/env python

"""
ldr2stl.py - An LDraw to STL convertor tool.

Copyright (C) 2009 Bryan Bishop <kanzure@gmail.com>

This file is part of the ldraw Python package.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import cmdsyntax
from ldraw.parts import Part, Parts, PartError
from ldraw.writers.stl import STLWriter
from ldraw import __version__


if __name__ == "__main__":

    syntax = "<LDraw parts file> <LDraw file> <STL file> <camera position> [--sky <sky colour>]"
    syntax_obj = cmdsyntax.Syntax(syntax)
    matches = syntax_obj.get_args(sys.argv[1:])
    
    if len(matches) != 1:
        sys.stderr.write("Usage: %s %s\n\n" % (sys.argv[0], syntax))
        sys.stderr.write("ldr2stl.py (ldraw package version %s)\n" % __version__)
        sys.stderr.write("Converts the LDraw file to an STL file.\n\n"
                         "The camera position is a single x,y,z argument where each coordinate\n"
                         "should be specified as a floating point number.\n"
                         "The optional sky colour is a single red,green,blue argument where\n"
                         "each component should be specified as a floating point number between\n"
                         "0.0 and 1.0 inclusive.\n\n")
        sys.exit(1)
    
    match = matches[0]
    parts_path = match["LDraw parts file"]
    ldraw_path = match["LDraw file"]
    stl_path = match["STL file"]
    camera_position = match["camera position"]
    
    parts = Parts(parts_path)
    
    try:
        model = Part(ldraw_path)
    except PartError:
        sys.stderr.write("Failed to read LDraw file: %s\n" % ldraw_path)
        sys.exit(1)
    
    stl_file = open(stl_path, "w")
    stl_file.write("solid lego\n")
    #pov_file.write('#include "colors.inc"\n\n')
    writer = STLWriter(parts, stl_file)
    writer.write(model)
    stl_file.write("endsolid lego")
    stl_file.close()
