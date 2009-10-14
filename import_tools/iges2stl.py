#!/usr/bin/python
#iges2stl in.iges out.stl
'''
iges2stl in.iges out.stl
converts from IGES to STL
'''
import sys
from OCC.Utils.DataExchange.IGES import IGESImporter
from OCC.Utils.DataExchange.STL import STLExporter
from OCC.BRepPrimAPI import *
from OCC.StlAPI import *

iges_file = sys.argv[1]
stl_file = sys.argv[2]

print "iges2stl: loading iges file"

my_iges_importer = IGESImporter(iges_file)
my_iges_importer.ReadFile()
the_shapes = my_iges_importer.GetShapes()
main_shape = the_shapes[0]

#Export to STL. If ASCIIMode is set to False, then binary format is used.
#my_stl_exporter = STLExporter(stl_file,ASCIIMode=True)
#my_stl_exporter.SetShape(the_compound)
#my_stl_exporter.WriteFile()

print "iges2stl: saving as stl"

stl_exp = StlAPI()
stl_exp.Write(main_shape, stl_file)

print "iges2stl: done"

