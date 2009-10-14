#!/usr/bin/python
#pov2png.py input.pov output.png
#TODO: automatically figure out the proper dimensions of the resulting image
import skdb.thirdparty.optfunc as optfunc
import os

def pov2png(pov_file, png_file):
    '''usage: %prog <pov_file> <png_file>
    converts from pov to a png file'''
    print "pov2png: starting"
    print "pov_file is: ", pov_file
    print "png_file is: ", png_file
    os.system("povray -d %s +O%s" % (pov_file, png_file))
    print "pov2png: done"

if __name__ == "__main__":
    optfunc.run(pov2png)
