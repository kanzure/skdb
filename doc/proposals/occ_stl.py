#!/usr/bin/python
#see http://www.opencascade.org/org/forum/thread_3145/
#thanks Patrik Muller
#FIXME: this takes about 20 to 40 seconds to read up any STL file.

path = "/home/kanzure/local/ldraw/pyldraw/ldraw-0.10/main/temp.stl"

import OCC.TCollection
import OCC.gp
import OCC.OSD
import OCC.RWStl
import OCC.TopoDS
import OCC.BRep
import OCC.StlMesh
import OCC.BRepBuilderAPI

occ_path = OCC.TCollection.TCollection_AsciiString(path)
osd_path = OCC.OSD.OSD_Path(occ_path)
rw = OCC.RWStl.RWStl()
my_mesh = rw.ReadAscii(osd_path)
my_mesh2 = OCC.StlMesh.Handle_StlMesh_Mesh(my_mesh).GetObject() #mesh mesh mesh
number_domains = my_mesh2.NbDomains()
p1 = OCC.gp.gp_XYZ()
p2 = OCC.gp.gp_XYZ()
p3 = OCC.gp.gp_XYZ()
vertex1 = OCC.TopoDS.TopoDS_Vertex()
vertex2 = OCC.TopoDS.TopoDS_Vertex()
vertex3 = OCC.TopoDS.TopoDS_Vertex()
akt_face = OCC.TopoDS.TopoDS_Face()
akt_wire = OCC.TopoDS.TopoDS_Wire()
builder = OCC.BRep.BRep_Builder()
#x1, y1, z1
#x2, y2, z2
#x3, y3, z3
x1,y1,z1,x2,y2,z2,x3,y3,z3 = 0, 0, 0, 0, 0, 0, 0, 0, 0

result_shape = OCC.TopoDS.TopoDS_Compound()
compound_builder = builder
compound_builder.MakeCompound(result_shape)

a_m_exp = OCC.StlMesh.StlMesh_MeshExplorer(my_mesh)
#print "debug1"

for iND in range(number_domains):
    #print "debug2"
    a_m_exp.InitTriangle(1)
    #print "debug3"
    while a_m_exp.MoreTriangle():
        (x1,y1,z1,x2,y2,z2,x3,y3,z3) = a_m_exp.TriangleVertices()
        p1.SetCoord(x1,y1,z1)
        p2.SetCoord(x2,y2,z2)
        p3.SetCoord(x3,y3,z3)
        if not p1.IsEqual(p2,0.0) and not p1.IsEqual(p3,0.0):
            vertex1 = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeVertex(OCC.gp.gp_Pnt(p1))
            vertex2 = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeVertex(OCC.gp.gp_Pnt(p2))
            vertex3 = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeVertex(OCC.gp.gp_Pnt(p3))
            akt_wire = OCC.BRepBuilderAPI.BRepBuilderAPI_MakePolygon(vertex1.Vertex(), vertex2.Vertex(), vertex3.Vertex(), True)
            #print "vertex1 = %s\nvertex2 = %s\nvertex3 = %s" % (p1.Coord(), p2.Coord(), p3.Coord())
            if akt_wire:#not akt_wire.IsNull():
                akt_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(akt_wire.Wire())
                #help(akt_face)
                if akt_face: #not akt_face.IsNull():
                    #print "debug4"
                    compound_builder.Add(result_shape, akt_face.Face())
                    #compound_builder.Add(OCC.TopoDS.TopoDS_Compound(), OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace().Shape())
                    #print "debug5"

        a_m_exp.NextTriangle()
true_result_shape = result_shape
print "done."

import OCC.Display.wxSamplesGui
OCC.Display.wxSamplesGui.display.DisplayShape(true_result_shape)
OCC.Display.wxSamplesGui.start_display()
