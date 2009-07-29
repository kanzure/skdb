#!/isr/bin/python
"""
stl.py - STL writer for the ldraw Python package.

Copyright (C) 2009 Bryan Bishop <kanzure@gmail.com>

This file is part of the ldraw Python package.

see pythonOCC/samples/Level2/DataExchange/import_stl.py

./ldr2stl.py /home/kanzure/local/ldraw/ldraw/even_more/LDRAW/parts.lst simple.ldr simple.stl
"""

from ldraw.geometry import Identity, Vector
from ldraw.parts import Parts, Quadrilateral, Triangle
from ldraw.pieces import Piece
import sys
import numpy

class STLWriter:
    def __init__(self, parts, stl_file):
        self.parts = parts
        self.stl_file = stl_file
        self.minimum = Vector(0, 0, 0)
        self.maximum = Vector(0, 0, 0)

    def write(self, model, current_matrix=Identity(), current_position=Vector(0,0,0), level=0):
        for obj in model.objects:
            if isinstance(obj, Piece):
                part = self.parts.part(code=obj.part)
                if part:
                    matrix = obj.matrix
                    self.write(part, current_matrix * matrix, current_position + current_matrix * obj.position, level+1)
                else:
                    sys.stderr.write("Part not found: %s\n" % obj.part)
            elif isinstance(obj, Triangle):
                p1 = current_matrix * obj.p1 + current_position
                p2 = current_matrix * obj.p2 + current_position
                p3 = current_matrix * obj.p3 + current_position
                if abs((p3 - p1).cross(p2-p1)) !=0:
                    self._write_triangle(p1, p2, p3)
            elif isinstance(obj, Quadrilateral):
                p1 = current_matrix * obj.p1 + current_position
                p2 = current_matrix * obj.p2 + current_position
                p3 = current_matrix * obj.p3 + current_position
                p4 = current_matrix * obj.p4 + current_position
                if abs((p3-p1).cross(p2-p1)) != 0:
                    self._write_triangle(p1,p2,p3)
                if abs((p3-p1).cross(p4-p1)) != 0:
                    self._write_triangle(p3, p4, p1)

    def _write_triangle(self, v1, v2, v3):
        self.minimum = Vector(min(self.minimum.x, v1.x, v2.x, v3.x), min(self.minimum.y, -v1.y, -v2.y, -v3.y), min(self.minimum.z, v1.z, v2.z, v3.z))
        self.maximum = Vector(max(self.maximum.x, v1.x, v2.x, v3.x), max(self.maximum.y, -v1.y, -v2.y, -v3.y), max(self.maximum.z, v1.z, v2.z, v3.z))
        #normal vector = cross product of any two of the edges
        #vec1 = p1-p2
        vec1 = numpy.matrix([v1.x-v2.x,v1.y-v2.y,v1.z-v2.z])
        #vec2 = p1-p3
        #vec2 = numpy.matrix([v1.x-v3.x,v1.y-v3.y,v1.z-v3.z])
        vec2 = numpy.matrix([v2.x-v3.x,v2.y-v3.y,v2.z-v3.z])
        #vec2 = numpy.matrix([v3.x-v1.x,v3.y-v1.y,v3.z-v1.z])

        normal_vector = numpy.cross(vec1, vec2)
        self.stl_file.write("facet normal %1.3f %1.3f %1.3f\n"
            "\touter loop\n"
            "\t\tvertex %1.3f %1.3f %1.3f\n"
            "\t\tvertex %1.3f %1.3f %1.3f\n"
            "\t\tvertex %1.3f %1.3f %1.3f\n"
            "\tendloop\n"
            "endfacet\n" % (normal_vector.item(0), normal_vector.item(1), normal_vector.item(2),
                          v1.x, -v1.y, v1.z,
                          v2.x, -v2.y, v2.z,
                          v3.x, -v3.y, v3.z)
                          )

