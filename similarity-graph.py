import os
import yaml
import graph

materials = yaml.load(open('materials.yaml'))

society = graph.graph()

for key in materials:
    if hasattr(materials[key], 'similar'):
        society.add_node(key)
        similar = materials[key].similar
        if hasattr(similar, '__getitem__'):
            friends = [i for i in similar]
        else:
            friendss = [similar]
        for friend in friends:
            society.add_node(friend)
            society.add_edge(key, friend)

suxxors = '''dotfile = open('/tmp/similarity-graph.dot', 'w')
dotfile.writelines(graph.readwrite.write_dot_graph(society, False))
dotfile.close()
tmp = os.popen('dot -Tpng -o similarity-graph.png')
'''

#run with: python build-similarity-graph.py  |dot -Tpng -o'foo.png
print graph.readwrite.write_dot_graph(society, False)
