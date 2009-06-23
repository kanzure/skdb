import os
import yaml
import graph

linnaeus = yaml.load(open('taxonomy.yaml'))

taxonomy = graph.graph()
node_id=0

def walk(treebeard, name, parent_node):
    global node_id
    try:
        #print treebeard.keys()
        for key in treebeard.keys():
            node_id += 1
            try:
                taxonomy.add_node(node_id, [('label', key)])
                taxonomy.add_edge(parent_node, node_id)#, label=key)
            except KeyError:
                #print 'yarrr:', parent_node, node_id, name
                pass
            walk(treebeard[key], key, node_id)
    except AttributeError: #leaf node
        node_id += 1
       #taxonomy.add_node(node_id, [('label', name)])
#print linnaeus['processes']['shaping']['joining']

taxonomy.add_node(node_id, [('label', 'root')])
walk(linnaeus['processes']['shaping']['joining'], 'root', node_id)
#walk(linnaeus['processes']['shaping'], 'root')
#print yaml.dump(taxonomy)
blarg = '''
for key in linnaeus:
    if hasattr(linnaeus[key], 'similar'):
        taxonomy.add_node(key)
        similar = materials[key].similar
        if hasattr(similar, '__getitem__'):
            friends = [i for i in similar]
        else:
            friendss = [similar]
        for friend in friends:
            society.add_node(friend)
            society.add_edge(key, friend)
'''
suxxors = '''dotfile = open('/tmp/similarity-graph.dot', 'w')
dotfile.writelines(graph.readwrite.write_dot_graph(society, False))
dotfile.close()
tmp = os.popen('dot -Tpng -o similarity-graph.png')
'''

#run with: python build-taxonomy-graph.py  |dot -Tpng -o'foo.png
print graph.readwrite.write_dot_graph(taxonomy, False)
