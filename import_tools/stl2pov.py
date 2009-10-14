#!/usr/bin/python
#stl2pov.py input.stl output.pov
#(this makes both output.pov.inc and output.pov)
import skdb.thirdparty.optfunc as optfunc
import os

#uses stl2pov
#http://www.xs4all.nl/~rsmith/software/stl2pov-2.4.3.tar.gz
#http://freshmeat.net/projects/stl2pov/

#stl2pov -s input.stl > output.inc
#include "rawr.inc"

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

if __name__ == "__main__":
    optfunc.run(stl2pov)

