#!/usr/bin/python
#original: http://web.media.mit.edu/~neilg/fab/dist/cam.py

class Stl:
    '''stl import export tools, does not depend on OCC'''
    def __init__(self, filename=None):
        self.filename = filename
        self.vertices, self.faces, self.boundarys, self.noise_flag = [], [], [], []
    def read(self):
        filename = self.filename
        vertices, faces, boundarys, noise_flag = self.vertices, self.faces, self.boundarys, self.noise_flag
        #
        # STL parser
        #
        noise_flag = 0
        vertex = 0
        vertices = []
        faces = []
        boundarys = []
        file = open(filename,'rb')
        str = file.read()
        file.close()
        if (find(str,"vertex") != -1):
           #
           # ASCII file
           #
           print "   ASCII file"
           file = open(filename,'r')
           str = file.readlines()
           file.close()
           line = 0
           nlines = len(str)
           while (line < nlines):
             if (find(str[line],'vertex') != -1):
              [vert, x, y, z] = split(str[line])
              x1 = float(x)
              y1 = float(y)
              z1 = float(z)
              vertices.append([x1,y1,z1])
              vertex += 1
              line += 1
              [vert, x, y, z] = split(str[line])
              x2 = float(x)
              y2 = float(y)
              z2 = float(z)
              vertices.append([x2,y2,z2])
              vertex += 1
              line += 1
              [vert, x, y, z] = split(str[line])
              x3 = float(x)
              y3 = float(y)
              z3 = float(z)
              vertices.append([x3,y3,z3])
              vertex += 1
              #faces.append([vertex-2,vertex-1,vertex,vertex-2])
              faces.append([vertex-2,vertex-1,vertex])
              line += 1
        else:
           #
           # binary file
           #
           nfacets = (len(str)-84)/50
           print "   binary file with",nfacets,"facets"
           for facet in range(nfacets):
              index = 84 + facet*50
              x1 = unpack('f',str[index+12:index+16])[0]
              y1 = unpack('f',str[index+16:index+20])[0]
              z1 = unpack('f',str[index+20:index+24])[0]
              vertices.append([x1,y1,z1])
              vertex += 1
              x2 = unpack('f',str[index+24:index+28])[0]
              y2 = unpack('f',str[index+28:index+32])[0]
              z2 = unpack('f',str[index+32:index+36])[0]
              vertices.append([x2,y2,z2])
              vertex += 1
              x3 = unpack('f',str[index+36:index+40])[0]
              y3 = unpack('f',str[index+40:index+44])[0]
              z3 = unpack('f',str[index+44:index+48])[0]
              vertices.append([x3,y3,z3])
              vertex += 1
              #faces.append([vertex-2,vertex-1,vertex,vertex-2])
              faces.append([vertex-2,vertex-1,vertex])
        self.vertices, self.faces, self.boundarys, self.noise_flag = vertices, faces, boundarys, noise_flag 

    def write_STL():
        faces, vertices, xmin, ymin, zmax = self.faces, self.vertices, self.xmin, self.ymin, self.zmax
        #
        # STL output
        #
        #text = outfile.get()
        file = open(self.filename, 'w')
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

