import os
import yaml
import graph
import random

depthcolors = {} #keeping track of colors per each level

def random_color(depth):
    '''A colorvalue may be  "h,s,v"  (hue,  saturation,  brightness)  floating
    point numbers between 0 and 1, or an X11 color name such as white black
    red green blue yellow magenta cyan or burlywood, or a  "#rrggbb"  (red,
    green, blue, 2 hex characters each) value.'''
    hue = random.uniform(0,1)
    saturation = random.uniform(0, 0.3)
    brightness = 0.9
    returnstring = '"%f,%f,%f"' % (hue, saturation, brightness)
    # set color to previous color at this depth (if exists)
    if depthcolors.has_key(depth):
        returnstring = (depthcolors[depth])[0]
        return returnstring
    # alt functionality: check if there's a color too similar already at this depth.
    # similarity means ?
    return returnstring

linnaeus = yaml.load(open('taxonomy.yaml'))

taxonomy = graph.digraph()
node_id=0 #we need numerical nodes because some terms show up multiple times, like thermal, mechanical, chemical

def walk(treebeard, color, parent_node, depth):
    global node_id
    try:
        for key in treebeard.keys():
            node_id += 1
            taxonomy.add_node(node_id, [('label', key), ('shape', 'box'),
                ('fontsize', '24'), ('color', color), ('style', 'filled')])
            taxonomy.add_edge(parent_node, node_id)
            color = random_color(depth)
            # make sure nothing with this same depth has this same color
            # or, make sure everything at this same depth has this same color
            if(depthcolors.has_key(depth)): depthcolors[depth].append(color)
            else: depthcolors[depth] = [color]
            walk(treebeard[key], color, node_id, depth+1)
    except AttributeError: #leaf node, need some way to peek at contents
        pass #node_id += 1

taxonomy.add_node(node_id, [('label', 'root')])
#walk(linnaeus['processes']['shaping']['joining'], 'root', node_id)
walk(linnaeus, 'yellow', node_id, 0)

#run with: python build-taxonomy-graph.py  |dot -Tpng -o'foo.png
print graph.readwrite.write_dot_graph(taxonomy, False)
