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
brick1.load_CAD()
brick2.load_CAD()

#display the original location of the first brick
pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(brick1.shapes[0],'RED')

#display an original location for the second brick (offset from the original brick, however)
transform0 = pymates.OCC.gp.gp_Trsf()
transform0.SetTranslation(pymates.OCC.gp.gp_Pnt(0,0,0),pymates.OCC.gp.gp_Pnt(0,10,0))
btr = pymates.OCC.BRepBuilderAPI.BRepBuilderAPI_Transform(transform0)
btr.Perform(brick2.shapes[0])
my_shape_for_brick2 = btr.Shape()
pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(my_shape_for_brick2,'GREEN')

res = pymates.mate_parts(part1=brick1, part2=brick2)
pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(res[0],'BLUE')
pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(res[1],'RED')
#pymates.show_interface_arrows()
pymates.draw_mating_arrows(brick1.interfaces[0], brick2.interfaces[5])
verty = pymates.make_vertex(pymates.OCC.gp.gp_Pnt(0,0,0))
pymates.OCC.Display.wxSamplesGui.display.DisplayShape(verty)

pymates.OCC.Display.wxSamplesGui.start_display()
