import os
import yaml
import graph
import random

def random_color():
    '''A colorvalue may be  "h,s,v"  (hue,  saturation,  brightness)  floating
    point numbers between 0 and 1, or an X11 color name such as white black
    red green blue yellow magenta cyan or burlywood, or a  "#rrggbb"  (red,
    green, blue, 2 hex characters each) value.'''
    hue = random.uniform(0,1)
    saturation = random.uniform(0, 0.3)
    brightness = 0.9
    return '"%f,%f,%f"' % (hue, saturation, brightness)

#linnaeus = yaml.load(open('processes_notags.yaml'))['abrasive jet']
linnaeus = yaml.load(open('taxonomy.yaml'))

taxonomy = graph.digraph()
node_id=0 #we need numerical nodes because some terms show up multiple times, like thermal, mechanical, chemical

def walk(treebeard, color, parent_node):
    global node_id
    children = []
    if hasattr(treebeard, 'keys'):
        children = treebeard.keys()
    for child in children:
        node_id += 1
        taxonomy.add_node(node_id, [('label', child), ('shape', 'box'),
            ('fontsize', '24'), ('color', color), ('style', 'filled')])
        taxonomy.add_edge(parent_node, node_id)
        #if hasattr(child, 'keys'): 
        walk(treebeard[child], random_color(), node_id)


taxonomy.add_node(node_id, [('label', 'root')])
#walk(linnaeus['processes']['shaping']['joining'], 'root', node_id)
walk(linnaeus, 'yellow', node_id)

#run with: python build-taxonomy-graph.py  |dot -G rankdir=LR -Tpng -o 'foo.png'
print graph.readwrite.write_dot_graph(taxonomy, False)
