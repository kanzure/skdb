"""
run: ipython -wthread -c "from pymates import pymates" -i

then copy/paste (lame) the following
"""

pymates.start()
from copy import deepcopy,copy
lego_pack = pymates.load_package("lego")
lego_pack.load_data()
brick1 = deepcopy(lego_pack.parts[0])
brick2 = deepcopy(lego_pack.parts[0])
brick1.post_init_hook()
brick2.post_init_hook()
brick1.load_CAD()
brick2.load_CAD()

#get the first part in the scene mating with a phantom "origin orientation interface"
blah = pymates.mate_first(brick1)
pymates.OCC.Display.wxSamplesGui.display.DisplayShape(blah)

options = brick1.options(brick2)
selected = list(options)[2]
selected.connect()
shape_thingy = pymates.mate_connection(selected)
pymates.OCC.Display.wxSamplesGui.display.DisplayShape(shape_thingy)
pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(brick1.shapes[0],'RED')
pymates.OCC.Display.wxSamplesGui.display.DisplayColoredShape(brick2.shapes[0], 'ORANGE')
