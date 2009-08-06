#!/usr/bin/python
import yaml
import  sys
from xml.dom import minidom
''''cat foo | heeks_coords.py' or 'heeks_coords.py foo.heeks' where foo.heeks
    is a HeeksCAD file containing coordinate systems you wish to inspect'''

def parse_file(file):
    coords = []
    doc = minidom.parse(file)
    for node1 in doc.childNodes:
        if node1.nodeName == 'HeeksCAD_Document':
            for node2 in node1.childNodes:
                if node2.nodeName == 'CoordinateSystem':
                    coords.append(parse_coord(node2))
    return coords

def parse_coord(node):
    tmp = {}
    attr_keys = ['ox', 'oy', 'oz', 'xx', 'xy', 'xz', 'yx', 'yy', 'yz']
    for key in attr_keys:
        attr = node.attributes[key]
        tmp[key] = float("%.13f" %(float(attr.value))) #round down to 0 if < +-1e-13
    
    return {'origin':[tmp['ox'], tmp['oy'], tmp['oz']],
            'x_vec':[tmp['xx'], tmp['xy'], tmp['xz']],
            'y_vec':[tmp['yx'], tmp['yy'], tmp['yz']],
            'name':str(node.attributes['title'].value)}

def main():
    rval = {}
    if len(sys.argv)>1 and sys.argv[1] == '-':
        rval['stdin'] = parse_file(sys.stdin)
    else:
        for i in sys.argv[1:]:
            rval[i] = parse_file(open(i))
    print yaml.dump(rval)
    return rval

if __name__ == '__main__':
   main()
