#based on a work by genehacker
#copyright 2009 ben lipkowitz
#distributed under the terms of the GNU GPL version 2 or later
#
#cycloidal.py: draws a cycloidal gear

import cairo
from math import *

def frange(start, stop, step): #this ought to come with python :(
    r = start
    while r < stop:
        yield r
        r += step

height, width = 500, 500
surf = cairo.SVGSurface('cycloidal.svg', height, width)
cr = cairo.Context(surf)
cr.translate(0.5, 0.5) #align pixels
cr.scale(width, height)
cr.translate(0.5, 0.5) #move gear to center of image

tmp = cr.user_to_device(1,1)
scale = (tmp[0] + tmp[1]) / 2.
cr.set_line_width(1/scale)
  
def cycloidal(teeth=17, module=0.05, resolution=2): 
    '''draws a cycloidal gear. arguments: number of teeth, circumference per tooth, degrees per step'''
    radius = module*teeth/2 #pitch radius
    z = teeth*2
    ro = radius/z #rolling circle radius
    inout = 1
    angle = 2*pi/z #angle of 1 lobe of hypo/epicycloid
    for m in range(z+1): #teeth):
        #for inout in [1, -1]:
            inout *= -1
            for theta in frange(angle*m, angle*(m+1), resolution*pi/180):
                x = ((radius + inout * ro) * cos(theta)) - inout * \
                        (ro * cos(theta * (radius + inout * ro)/ro))
                y = ((radius + inout * ro) * sin(theta)) - \
                        (ro * sin(theta * (radius + inout * ro)/ro))
                if m == 0: 
                    cr.move_to(x, y)
                else: 
                    cr.line_to(x,y)
    cr.set_source_rgb(1,1,1)
    cr.fill_preserve()
    cr.set_source_rgb(0,0,0)
    cr.stroke()

cycloidal(10)
cycloidal(8)
surf.write_to_png('cycloidal.png')
