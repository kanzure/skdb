#!/usr/bin/env python
"""
occ-pyldraw.py - an LDRAW to pythonOCC tool.

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
import cmdsyntax
import numpy
from ldraw.geometry import Identity, Vector
from ldraw.parts import Part, Parts, PartError, Quadrilateral, Triangle
from ldraw.pieces import Piece
from ldraw import __version__

#see second to last post here (Marcel Janer):
#http://www.opencascade.org/org/forum/thread_9793/
if __name__ == "__main__":

    syntax = "<LDraw parts file> <LDraw file> <STL file> <camera position> [--sky <sky colour>]"
    syntax_obj = cmdsyntax.Syntax(syntax)
    matches = syntax_obj.get_args(sys.argv[1:])
    
    if len(matches) != 1:
        sys.stderr.write("Usage: %s %s\n\n" % (sys.argv[0], syntax))
        sys.stderr.write("ldr2stl.py (ldraw package version %s)\n" % __version__)
        sys.stderr.write("Converts the LDraw file to an STL file.\n\n"
                         "The camera position is a single x,y,z argument where each coordinate\n"
                         "should be specified as a floating point number.\n"
                         "The optional sky colour is a single red,green,blue argument where\n"
                         "each component should be specified as a floating point number between\n"
                         "0.0 and 1.0 inclusive.\n\n")
        sys.exit(1)
    
    match = matches[0]
    parts_path = match["LDraw parts file"]
    ldraw_path = match["LDraw file"]
    stl_path = match["STL file"]
    camera_position = match["camera position"]
    
    parts = Parts(parts_path)
    
    try:
        model = Part(ldraw_path)
    except PartError:
        sys.stderr.write("Failed to read LDraw file: %s\n" % ldraw_path)
        sys.exit(1)
    
    #pov_file.write('#include "colors.inc"\n\n')
    writer = OCC_Writer(parts)
    writer.write(model)

class OCC_Writer:
    def __init__(self, parts):
        self.parts = parts
        #create an empty mesh
        self.occ_model = OCC.Utils.DataExchange.StlMesh.StlMesh_Mesh()

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

#OCC.GeomAPI.GeomAPI_PointsToBSplineSurface(
##optional -> OCC.BRepBuilderAPI.BRepBuilderAPI_MakeVertex(some point)
#edge1 = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge(P1,P2)
#wire1 = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeWire()
#wire1.Add(ExistingWire1)
#wire1.Add(edge1)
#wire1.Wire() <- shape object
#wire1.Edge() <- shape object
#wire1.Vertex() <- shape object
#my_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(wire1)
##optional?
#BRepLib.BuildCurves3d(my_face.Face())

    def draw(self):
        #aMesh = MeshVS_Mesh()
        my_mesh = OCC.MeshVS.MeshVS_Mesh()
        #aDS = XSDRAWSTLVRML_DataSource( aStlMesh )

        #aMesh.SetDataSource(aDS)
        
        #aMesh.AddBuilder( MeshVS_MeshPrsBuilder(aMesh), True)
        #aMesh.GetDrawer().SetBoolean(MeshVS_DA_DisplayNodes, False)
        #aMesh.GetDrawer().SetBoolean(MeshVS_DA_ShowEdges, False)
        #aMesh.GetDrawer().SetBoolean(MeshVS_DA_FrontMaterial, DEFAULT_MATERIAL)
        #aMesh.SetColor(Quantity_NOC_AZURE)
        #aMesh.SetDisplayMode(MeshVS_DMF_Shading) #mode as default
        #aMesh.SetHilightMode(MeshVS_DMF_WireFrame) #wireframe as default hilight mode
        #myDoc.m_AISContext.Display(aMesh)



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
        return self.occ_model

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

