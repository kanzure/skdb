#!/usr/bin/python
'''
vizlegos.py - pyldraw visualization tool :)

Bryan Bishop <kanzure@gmail.com>
2009-08-01

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from ldraw.geometry import Identity, Vector
from ldraw.parts import Part, Parts, PartError, Quadrilateral, Triangle
from ldraw.pieces import Piece
import numpy
import visual

#TODO: see visual.faces(pos=[],normals=[])

#config
parts_path = "/home/kanzure/local/ldraw/ldraw/even_more/LDRAW/parts.lst"
ldraw_path = "/home/kanzure/local/ldraw/pyldraw/ldraw-0.10/main/temp.ldr"

class Visualizer:
    def __init__(self, parts):
        self.parts = parts
        #see http://vpython.org/contents/docs/visual/faces.html
        self.positions = []
        self.normals = []
    def write(self, model, current_matrix=Identity(), current_position=Vector(0,0,0), level=0):
        for obj in model.objects:
            if isinstance(obj, Piece):
                part = self.parts.part(code=obj.part)
                if part:
                    matrix = obj.matrix
                    blah = current_position + current_matrix * obj.position
                    self.write(part, current_matrix * matrix, blah, level+1)
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
        #the moment of truth
        visual.faces(pos=self.positions, normal=self.normals)
    def _write_triangle(self, v1, v2, v3):
        vec1 = numpy.matrix([v1.x-v2.x,v1.y-v2.y,v1.z-v2.z])
        vec2 = numpy.matrix([v2.x-v3.x,v2.y-v3.y,v2.z-v3.z])
        normal_vector = numpy.cross(vec1, vec2)
        self.positions.append((v1.x,v1.y,v1.z))
        self.positions.append((v2.x,v2.y,v2.z))
        self.positions.append((v3.x,v3.y,v3.z))
    
        self.normals.append((normal_vector.item(0), normal_vector.item(1), normal_vector.item(2)))
        self.normals.append((normal_vector.item(0), normal_vector.item(1), normal_vector.item(2)))
        self.normals.append((normal_vector.item(0), normal_vector.item(1), normal_vector.item(2)))

parts = Parts(parts_path, filename=True)
try:
    model = Part(ldraw_path, filename=True)
except PartError:
    sys.stderr.write("Failed to read LDraw file: %s\n" % ldraw_path)
    sys.exit(1)

writer = Visualizer(parts)
writer.write(model)

