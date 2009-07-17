#!/usr/bin/python
import yaml
import pymates
import settings

block = pymates.Part(name="block with hole", cadfile="http://adl.serveftp.org/lab/models/blockwithhole.iges")
peg = pymates.Part(name="peg", cadfile="http://adl.serveftp.org/lab/models/peg.iges")

possibilities = pymates.compatibility(block, peg, block.ports[1], peg.ports[3])
possibilities = pymates.compatibility(block, peg, block.ports[5], peg.ports[0])
possibilities = pymates.compatibility(block, peg)

for each in possibilities:
    complex_geom = fuse(block, peg, way=each)
    volume_diff = pymates.algorithms.calculate_volume_difference(complex_geom)
    total_volume = pymates.algorithms.calculate_volume_total(complex_geom)
    if settings.mode == 'pythonOCC': #we're in pythonOCC
        display.__draw3d__(each) #draw the possibility
    elif settings.mode == 'shell': #non-graphical
        #assuming it has a nice __repr__ method definition
        print each
    elif settings.mode == 'web':
        #generate svg and cache?
        #generate 3D rendering and cache?
        pass
    pass
