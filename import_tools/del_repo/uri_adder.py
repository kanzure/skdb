import graphsynth

filename = "VWBugCarburetorCFG.xml"

def construct_uri(some_string, assembly_name):
    return "http://utdesign.org/skdb-packages/VOICED/Assemblies/" + assembly_name + "/components/" + some_string + ".yaml"

#load the graph
my_graph = graphsynth.Graph.load_gxml(filename)

#make the assembly name for construct_uri
assembly_name = filename.replace(".gxml", "")

for node in my_graph.nodes:
    try:
        cb_name = node.local_labels[0]
    
        #construct the ur iname
        uri = construct_uri(cb_name, assembly_name)
        node.local_labels[1] = uri
    except:
        print "wah!"

#now save the graph
my_graph.save_gxml("output_" + filename)


