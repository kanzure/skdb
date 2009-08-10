#!/usr/bin/python
#this is so that I do not have to go through the GUI every other minute to test something

import pymates
import skdb

pymates.start()
#pymates.demo()
foo = skdb.load_package("lego")
brick1 = skdb.load(open("../packages/lego/data.yaml"))["parts"][0]
brick2 = skdb.load(open("../packages/lego/data.yaml"))["parts"][0]
pymates.register_part(brick1)
pymates.register_part(brick2)
#brick1.load_CAD()
#brick2.load_CAD()
#display brick1
#pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(brick1.shapes[0], 'RED')
#res = pymates.mate_parts(part1=brick1, part2=brick2)
#pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(res.Shape(),'BLUE')
#pymates.show_interface_arrows()
pymates.draw_mating_arrows(brick1.interfaces[0], brick2.interfaces[0])
pymates.OCC.Display.wxSamplesGui.start_display()
