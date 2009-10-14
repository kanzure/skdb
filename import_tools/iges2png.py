#!/usr/bin/python
#iges2png.py input.iges output.png
#leaves behind: output.png, output.png.pov, output.png.pov.inc
import sys, os
from OCC.Utils.DataExchange.IGES import IGESImporter
from OCC.Utils.DataExchange.STL import STLExporter
from OCC.BRepPrimAPI import *
from OCC.StlAPI import *
import skdb.thirdparty.optfunc as optfunc

#http://freshmeat.net/projects/stl2pov/
#http://www.xs4all.nl/~rsmith/software/stl2pov-2.4.3.tar.gz

def iges2png(iges_file, png_file):
    '''usage: %prog <iges_file> <png_file>
    converts from IGES to PNG
    
    stuff it leaves behind:
        input.iges.stl
        input.iges.pov
        input.iges.pov.inc
        output.png'''

    print "iges2png: loading iges file."
    my_iges_importer = IGESImporter(iges_file)
    my_iges_importer.ReadFile()
    the_shapes = my_iges_importer.GetShapes()
    main_shape = the_shapes[0]

    print "iges2png: saving iges as stl."
    stl_exp = StlAPI()
    stl_exp.Write(main_shape, iges_file + ".stl")
    
    print "iges2png: converting stl to pov"
    stl2pov(iges_file + ".stl", iges_file + ".pov")

    print "iges2png: converting pov to png"
    pov2png(iges_file + ".pov", png_file)

    print "iges2png: done"

def stl2pov(stl_file, pov_file):
    '''usage: stl2pov.py input.stl output.pov
    makes both output.pov and output.pov.inc'''
    os.system("stl2pov -s %s > %s.inc" % (stl_file, pov_file))
    pov_template = '''#include "%s.inc"

    background{color rgb 1 }    

    object{  m_facet 
    rotate 90*x

    texture{  pigment{ color rgb <1,0.5,0> }
             finish {   ambient 0.15
                        diffuse 0.85
                        specular 0.3 } } } 

    light_source {  <-20,100,20>  color rgb 2}  

    camera {
    perspective
      angle 0
      right x*image_width/image_height
      location <-100,50,10>
      look_at y
    }''' % (pov_file)

    pov_file = open(pov_file, "w")
    pov_file.write(pov_template)
    pov_file.close()

def pov2png(pov_file, png_file):
    '''usage: %prog <pov_file> <png_file>
    converts from pov to a png file'''
    print "pov2png: starting"
    print "pov_file is: ", pov_file
    print "png_file is: ", png_file
    os.system("povray -d %s +O%s" % (pov_file, png_file))
    print "pov2png: done"

if __name__ == "__main__":
    optfunc.run(iges2png)
