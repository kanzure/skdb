#!/usr/bin/python
#http://web.media.mit.edu/~neilg/fab/dist/cam.py/STL

def write_STL():
   global faces, vertices, xmin, ymin, zmax
   #
   # STL output
   #
   text = outfile.get()
   file = open(text, 'w')
   file.write("solid\n")
   xyscale = float(sxyscale.get())
   zscale = float(szscale.get())
   xoff = float(sxmin.get()) - xmin*xyscale
   yoff = float(symin.get()) - ymin*xyscale
   zoff = float(szmax.get()) - zmax*zscale
   #
   # scale vertices
   #
   for vertex in range(len(vertices)):
      x = vertices[vertex][X]*xyscale + xoff
      y = vertices[vertex][Y]*xyscale + yoff
      z = vertices[vertex][Z]*zscale + zoff
      vertices[vertex] = [x,y,z]
   #
   # write file
   #
   nfaces = len(faces)
   for face in range(nfaces):
      #
      # find normal
      #
      [x0,y0,z0] = vertices[faces[face][0]-1]
      [x1,y1,z1] = vertices[faces[face][1]-1]
      [x2,y2,z2] = vertices[faces[face][2]-1]
      """
      [nx,ny,nz] = [-x0, -y1, -z2]
      [d1x,d1y,d1z] = [x1-x0, y1-y0, z1-z0]
      d1 = d1x*d1x + d1y*d1y + d1z*d1z
      nd1 = nx*d1x + ny*d1y + nz*d1z
      [nx,ny,nz] = [nx-nd1*d1x/d1, ny-nd1*d1y/d1, nz-nd1*d1z/d1]
      [d2x,d2y,d2z] = [x2-x0, y2-y0, z2-z0]
      d2d1 = d2x*d1x + d2y*d1y + d2z*d1z
      [d2x,d2y,d2z] = [d2x-d2d1*d1x/d1, d2y-d2d1*d1y/d1, d2z-d2d1*d1z/d1]
      d2 = d2x*d2x + d2y*d2y + d2z*d2z
      nd2 = nx*d2x + ny*d2y + nz*d2z
      [nx,ny,nz] = [nx-nd2*d2x/d2, ny-nd2*d2y/d2, nz-nd2*d2z/d2]
      n = sqrt(nx*nx + ny*ny + nz*nz)
      [nx,ny,nz] = [nx/n, ny/n, nz/n]
      """
      [nx,ny,nz] = [0,0,0]
      #
      # write
      #
      file.write("   facet normal %f %f %f\n"%(nx,ny,nz))
      file.write("      outer loop\n")
      file.write("         vertex %f %f %f\n"%(x0,y0,z0))
      file.write("         vertex %f %f %f\n"%(x1,y1,z1))
      file.write("         vertex %f %f %f\n"%(x2,y2,z2))
      file.write("      endloop\n")
      file.write("   endfacet\n")
      if (len(faces[face]) == 4):
         #
         # triangulate square face
         #
         [x3,y3,z3] = vertices[faces[face][3]-1]
         file.write("   facet normal %f %f %f\n"%(nx,ny,nz))
         file.write("      outer loop\n")
         file.write("         vertex %f %f %f\n"%(x0,y0,z0))
         file.write("         vertex %f %f %f\n"%(x2,y2,z2))
         file.write("         vertex %f %f %f\n"%(x3,y3,z3))
         file.write("      endloop\n")
         file.write("   endfacet\n")
   file.write("endsolid\n")
   file.close()
   print "wrote",nfaces,"STL facets to",text

