#!/usr/bin/python
#http://web.media.mit.edu/~neilg/fab/dist/cam.py

def read_STL(filename):
   global vertices, faces, boundarys, noise_flag
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
#       faces.append([vertex-2,vertex-1,vertex,vertex-2])
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
#    faces.append([vertex-2,vertex-1,vertex,vertex-2])
     faces.append([vertex-2,vertex-1,vertex])

