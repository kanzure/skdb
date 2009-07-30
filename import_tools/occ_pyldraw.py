#!/usr/bin/env python
"""
occ_pyldraw.py - an LDRAW to pythonOCC tool.

this is very, very slow. :( how can it be improved?
    - see skdb/doc/proposals/occ_stl.py (which is also slow)

Copyright (C) 2009 Bryan Bishop <kanzure@gmail.com>

This file is part of the ldraw Python package.

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
"""

import sys
import numpy
#import OCC.BRepBuilderAPI
#import OCC.BRepPrimAPI
#import OCC.gp
from ldraw.geometry import Identity, Vector
from ldraw.parts import Part, Parts, PartError, Quadrilateral, Triangle
from ldraw.pieces import Piece
from ldraw import __version__
import copy
#see second to last post here (Marcel Janer):
#http://www.opencascade.org/org/forum/thread_9793/
def draw_it(ldr,OCC):
    parts_path = "/home/kanzure/local/ldraw/ldraw/even_more/LDRAW/parts.lst"
    ldraw_path = ldr #might not be a path though (in this case, it's definitely *not* a path)
    
    parts = Parts(parts_path, filename=False) #might not be a path though (ok, it handles this case now)
    
    try:
        model = Part(ldraw_path, filename=False)
    except PartError:
        sys.stderr.write("Failed to read LDraw file: %s\n" % ldraw_path)
        sys.exit(1)
    
    #pov_file.write('#include "colors.inc"\n\n')
    writer = OCC_Writer(parts,OCC)
    writer.write(model)
    main_shape = OCC.TopoDS.TopoDS_Shape()
    for shape in writer.all_shapes:
        
        main_shape = OCC.BRepAlgoAPI.BRepAlgoAPI_Fuse(copy.copy(main_shape), shape)
        main_shape = copy.copy(main_shape).Shape()
        #self.OCC.Display.wxSamplesGui.display.DisplayShape(face.Shape())
    while main_shape.IsDone()==0:
        print "blah2"
    OCC.Display.wxSamplesGui.display.DisplayShape(main_shape.Shape())

class OCC_Writer:
    def __init__(self, parts, OCC):
        self.parts = parts
        self.OCC = OCC
        self.all_shapes = []
        #create an empty mesh
        #FIXME: StlMesh can't be converted (easily)
        #self.occ_model = OCC.Utils.DataExchange.StlMesh.StlMesh_Mesh()

#http://www.opencascade.org/org/forum/thread_6904/
#You can try creating edges for your triangles from your triangle
#points, connecting those edges to make wires, creating faces from
#the edges, and then shells from the faces. You can then perform
#boolean operations on the shells or create solids from the shells
#and perform boolean operations on the solids. Understand that the
#boolean operations may be slow since there could be a large number
#of faces in your geometry.
#
#The classes you will be concerned with are the BRepBuilderAPI_MakeXXX
#where XXX is Edge, Wire, Face, Shell, and Solid.
#
#Some shortcuts could be to use BRepBuilderAPI_MakePolygon to create
#a wire directly from 3 points (note that the points must be planar).
#
#I hope this gets you started.

#see also: pythonOCC/samples/Level1/TopologyBuilding/topology_building.py
#in particular, edge(), wire(), and face()

    def write(self, model, current_matrix=Identity(), current_position=Vector(0,0,0), level=0):
        '''write the model to the OpenCASCADE API'''
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
        #return self.occ_model
    def _write_triangle(self, v1, v2, v3):
        p1 = self.OCC.gp.gp_Pnt(v1.x,v1.y,v1.z)
        p2 = self.OCC.gp.gp_Pnt(v2.x,v2.y,v2.z)
        p3 = self.OCC.gp.gp_Pnt(v3.x,v3.y,v3.z)
        vec1 = numpy.matrix([v1.x-v2.x,v1.y-v2.y,v1.z-v2.z])
        vec2 = numpy.matrix([v2.x-v3.x,v2.y-v3.y,v2.z-v3.z])
        normal_vector = numpy.cross(vec1, vec2)

        #OCC.GeomAPI.GeomAPI_PointsToBSplineSurface(
        ##optional -> OCC.BRepBuilderAPI.BRepBuilderAPI_MakeVertex(some point)
        #edge1 = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge(P1,P2)
        edge1 = self.OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge(p1,p2)
        edge2 = self.OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge(p2,p3)
        edge3 = self.OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge(p1,p3)
        #wire1 = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeWire()
        wire1 = self.OCC.BRepBuilderAPI.BRepBuilderAPI_MakeWire()
        #wire1.Add(ExistingWire1)
        #wire1.Add(edge1)
        wire1.Add(edge1.Edge())
        wire1.Add(edge2.Edge())
        wire1.Add(edge3.Edge())
        #wire1.Wire() <- shape object
        #wire1.Edge() <- shape object
        #wire1.Vertex() <- shape object
        #my_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(wire1.Wire())
        face1 = self.OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(wire1.Wire())
        geom_surface = self.OCC.BRep.BRep_Tool().Surface(face1.Face()) #returns Handle_Geom_Surface
        shell1 = self.OCC.BRepBuilderAPI.BRepBuilderAPI_MakeShell(geom_surface)
        #TODO: make shells from the faces
        #shell1 = self.OCC.BRepPrimAPI.BRepPrimAPI_MakePrism(wire1.Shape(), self.OCC.gp.gp_Vec(normal_vector.item(0),normal_vector.item(1),normal_vector.item(2)))
        #TODO: create solids from the shells (thanks Rob Bachrach)
        #self.OCC.Display.wxSamplesGui.display.DisplayShape(face1.Shape())
        self.all_shapes.append(face1.Face())

        return face1


    def write_old(self, model, current_matrix=Identity(), current_position=Vector(0,0,0), level=0):
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
        return self.occ_model

    def _write_triangle_old(self, v1, v2, v3):
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

        #StlMesh_MeshTriangle (const Standard_Integer V1, const Standard_Integer V2, const Standard_Integer V3, const Standard_Real Xn, const Standard_Real Yn, const Standard_Real Zn)
        self.occ_model.AddTriangle(vec1.item(0), vec1.item(1), vec1.item(2), vec2.item(0), vec2.item(1), vec2.item(2), normal_vector.item(0), normal_vector.item(1), normal_vector.item(2))

#        self.stl_file.write("facet normal %1.3f %1.3f %1.3f\n"
#            "\touter loop\n"
#            "\t\tvertex %1.3f %1.3f %1.3f\n"
#            "\t\tvertex %1.3f %1.3f %1.3f\n"
#            "\t\tvertex %1.3f %1.3f %1.3f\n"
#            "\tendloop\n"
#            "endfacet\n" % (normal_vector.item(0), normal_vector.item(1), normal_vector.item(2),
#                          v1.x, -v1.y, v1.z,
#                          v2.x, -v2.y, v2.z,
#                          v3.x, -v3.y, v3.z)
#                          )

