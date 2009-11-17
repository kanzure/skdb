#!/usr/bin/python
"""
/**************************************************************************
 *     GraphSynth is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *  
 *     GraphSynth is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *  
 *     You should have received a copy of the GNU General Public License
 *     along with GraphSynth.  If not, see <http://www.gnu.org/licenses/>.
 *     
 *     Please find further details and contact information on GraphSynth
 *     at: http://graphsynth.com/
 *     
 *     Original author: Matthew Ira Campbell <mc1@mail.utexas.edu>
 *     Python translation by: Bryan Bishop <kanzure@gmail.com>
 *************************************************************************/
"""
import math
import os
import yaml #maybe one day?
from numpy import identity, multiply
from copy import copy
import functools
import unittest

#for xml
from xml.dom import minidom

campbell_message = "campbell didnt implement this"
bryan_message = "bryan hasnt got this far yet"
def bryan_message_generator(path): return bryan_message + (" (%s)" % (path))

#in the original graphsynth codebase, there were a lot of properties
#these need to be reincorporated into this python version
def _set_property(self, value=None, attribute_name=None, attr_index=None):
    assert attribute_name, "_set_property must have an attribute name to work with"
    if attr_index is not None:
        self.__getattribute__(attribute_name)[attr_index] = value
    else:
        setattr(self, attribute_name, value)
def _get_property(self, attribute_name=None, attr_index=None):
    assert attribute_name, "_get_attribute must have an attribute name to work with"
    if attr_index is not None:
        return self.__getattribute__(attribute_name)[attr_index]
    return getattr(self, attribute_name)
class PropertyExample:
    x = property(fget=functools.partial(_set_property, attribute_name='x'), fset=functools.partial(_get_property, attribute_name='x'), doc="represents the x coordinate of the PropertyExample object")

class TestPythonStuff(unittest.TestCase):
    def test_properties(self):
        test_message = "testing 123"
        prop_ex = PropertyExample()
        self.assertTrue(prop_ex.x == None)
        prop_ex.x = test_message
        self.assertTrue(prop_ex.x == test_message)
if __name__ == "__main__":
    unittest.main()

class TestGraphSynth(unittest.TestCase):
    def test_graph(self):
        g1 = Graph()
    def test_node(self):
        n1 = Node()
    def test_arc(self):
        a1 = Arc()
    def test_rule(self):
        r1 = Rule()
    def test_rule_set(self):
        r1 = Rule()
        r2 = Rule()
        s1 = RuleSet()
    def test_recognize_choose_apply(self):
        pass

def find_delegate(some_list, example):
    '''returns a sublist of some_list where the attributes of the elements match those of the example
    for example:
        >>>class Foo:
        >>>    def __init__(self, name=""):
        >>>        self.name = name
        >>>class Bar:
        >>>    name = "hello"
        >>>find_delegate([Foo(name="hello"), Foo(name="hello1")], Bar())
        <Foo>
    '''
    assert hasattr(example, "__dict__"), "find_delegate: matching object must have a __dict__"
    #get a list of extra attributes
    relevant_keys = []
    for key in example.__dict__.keys():
        if key.count("_") == 0:
            relevent_keys.append(key)
    if len(relevant_keys)==0: return some_list
    results = []
    for option in some_list:
        assert hasattr(option, "__dict__"), "find_delegate: objects to search must have a __dict__"
        for key in relevant_keys:
            if option.__dict__.has_key(key):
                if option.__dict__[key] == example.__dict__[key]:
                    results.append(option)
    return results

class NextGenerationSteps:
    loop = 1
    go_to_next = 2
    go_to_previous = 3
class CandidatesAre:
    unspecified = 1

def set_list(self, variable, index, label):
    '''called a few times in Arc, like in set_label and set_variable'''
    while len(variable) <= index:
        variable.append("")
    variable[index] = label

def make_identity(size):
    return identity(size)

class Arc:
    graphsynth_path = "GraphSynth.Representation/BasicGraphClasses/arc.cs"
    def __init__(self, name="", from_node=None, to_node=None, directed=False, doubly_directed=False, local_labels=[], local_variables=[], old_data={'style_key': "", 'x': "", 'y': ""}):
        self.name = name
        self._from = from_node #tail
        self._to = to_node #head
        self.directed = directed
        self.doubly_directed = doubly_directed
        self.local_labels = local_labels
        self.local_variables = local_variables
        self.old_data = old_data

    def set_to(self, to):
        self._to = to
    def set_from(self, from1):
        self._from = from1
    def get_from(self):
        return self._from
    def get_to(self):
        return self._to
    def length(self):
        '''if _to and _from are not nodes, calculate a distance'''
        assert not isinstance(self._to, Node)
        assert not isinstance(self._from, Node)
        v1 = self._from
        v2 = self._to
        return math.sqrt((v1.X - v2.X) * (v1.X - v2.X) + (v1.Y - v2.Y) * (v1.Y - v2.Y))
    def other_node(self, node1):
        '''returns the other node that this edge connects to.
        returns True if both nodes are the same as the input node'''
        if self._to == self._from and self._from == node1: return True
        if node1 == self._to: return self._from
        elif node1 == self._from: return self._to
        else: raise ValueError, "Arc.other_node thinks this node isn't the 'to' and it isn't the 'from'. what is it?"
    def set_label(self, index, label):
        '''set the label with an index of 'index' to label'''
        set_list(self.local_labels, index, label)
    def set_variable(self, index, variable):
        set_list(self.local_variables, index, variable)
    def to_gxml(self):
        '''returns gxml including <arc> and </arc>'''

        output = "<arc>\n"
        #name
        output = output + "<name>" + str(self.name) + "</name>\n"
        #localVariables
        if len(self.local_variables) == 0: output = output + "<localVariables />\n"
        else:
            output = output + "<localVariables>\n"
            for local_var in self.local_variables:
                output = output + "<localVariable>" + str(local_var) + "</localVariable>\n"
            output = output + "</localVariables>\n"
        #localLabels
        if len(self.local_labels) == 0: output = output + "<localLabels />\n"
        else:
            output = output + "<localLabels>\n"
            for local_label in self.local_labels:
                output = output + "<localLabel>" + str(local_label) + "</localLabel>\n"
            output = output + "</localLabels>\n"
        #From
        if self._from == None: output = output + "<From></From>\n"
        else: output = output + "<From>" + str(self._from.name) + "</From>\n"
        #To
        if self._to == None: output = output + "<To></To>\n"
        else: output = output + "<To>" + str(self._to) + "</To>\n"
        #directed
        output = output + "<directed>" + str(self.directed).lower() + "</directed>\n"
        #doublyDirected
        output = output + "<doublyDirected>" + str(self.doublyDirected).lower() + "</doublyDirected>\n"

        output = output + "</arc>\n"
        return output

class Edge(Arc):
    '''Originally, I created a separate edge and vertex class to allow for the future expansion of GraphSynth into shape grammars. I now have decided that the division is not useful, since it simply deprived nodes of X,Y,Z positions. Many consider edge and arc, and vertex and node to be synonymous anyway but I prefer to think of edges and vertices as arcs and nodes with spatial information. At any rate there is no need to have these inherited classes, but I keep them for backwards-compatible purposes.'''
    #there isn't actually any code for an Edge
    graphsynth_path = "GraphSynth.Representation/BasicGraphClasses/arc.cs"
    pass    

class Node:
    graphsynth_path = "GraphSynth.Representation/BasicGraphClasses/node.cs"
    #none of this has to be here, it's just for reference
    arcs = [] #list of arcs connecting to this node
    arcs_to = [] #those arcs where arc._to points to this node. "head of the arc".
    arcs_from = [] #those arcs where arc._from points to this node. "tail of the arc".
    X, Y, Z = 0,0,0 #In an effort to move towards shape grammars, I have decided to make the X, Y, and Z positions of a node permanent members of the node class. This transition will not affect any existing graph grammars, but will allow future graph grammars to take advantage of relative positioning of new nodes. Additionally, it solves the problem of getting X, Y, and Z into the ruleNode class.
    old_data = {'screenX': 0, 'screenY': 0}

    def __init__(self, name="", local_labels=[], local_variables=[], arcs=[], arcs_to=[], arcs_from=[], X=0, Y=0, Z=0, old_data={'screenX':0, 'screenY':0}):
        self.name = name
        self.local_labels = local_labels
        self.local_variables = local_variables
        self.arcs = arcs
        self.arcs_to = arcs_to
        self.arcs_from = arcs_from
        self.X = X
        self.Y = Y
        self.Z = Z
        self.old_data = old_data
    def degree(self):
        '''the degree or valence of a node is the number of arcs attached to it.
        currently this is used in recognition of rule when the strictDegreeMatch is True.'''
        return len(self.arcs)
    def to_gxml(self):
        '''returns gxml including <node> and </node>'''

        output = "<node>\n"
        #name
        output = output + "<name>" + str(self.name) + "</name>\n"
        #localVariables
        if len(self.local_variables) == 0: output = output + "<localVariables />\n"
        else:
            output = output + "<localVariables>\n"
            for local_var in self.local_variables:
                output = output + "<localVariable>" + str(local_var) + "</localVariable>\n"
            output = output + "</localVariables>\n"
        #localLabels
        if len(self.local_labels) == 0: output = output + "<localLabels />\n"
        else:
            output = output + "<localLabels>\n"
            for local_label in self.local_labels:
                output = output + "<localLabel>" + str(local_label) + "</localLabel>\n"
            output = output + "</localLabels>\n"

        #do X, Y, Z if it has that information
        if hasattr(self, "X"): output = output + "<X>" + str(self.X) + "</X>\n"
        if hasattr(self, "Y"): output = output + "<Y>" + str(self.Y) + "</Y>\n"
        if hasattr(self, "Z"): output = output + "<Z>" + str(self.Z) + "</Z>\n"

        output = output + "</node>\n"
        return output

    set_label = Arc.set_label
    set_variable = Arc.set_variable

class Vertex(Node):
    #this was blank in the graphsynth codebase for some reason?
    graphsynth_path = "GraphSynth.Representation/BasicGraphClasses/node.cs"
    pass

class Graph:
    graphsynth_path = "GraphSynth.Representation/BasicGraphClasses/designGraph.cs"
    def __init__(self, count=None, nodes=None, arcs=None, global_labels=[], global_variables=[]):
        '''set count to some number to make this a complete graph of that many nodes.
        note: average_degree is currently not implemented (to make a graph with an average degree on each node)
        '''
        self.global_labels = global_labels
        self.global_variables = global_variables
        self.arcs = []
        self.nodes = []
        if count is not None:
            assert isinstance(count, int)
            for i in range(count):
                self.add_node()
            for node in self.nodes:
                for node2 in self.nodes[1:]:
                    self.add_arc("seed arc " + len(self.arcs), node, node2)
            return
        if nodes is not None and arcs is not None:
            self.nodes.extend(nodes)
            self.arcs.extend(arcs)
    @staticmethod
    def _check_for_repeat_names(the_array):
        '''warning: this also fixes the repeat names.'''
        any_name_changed = False
        for node1 in the_array:
            name_changed = False
            for node2 in the_array[1:]:
                if node1.name == node2.name:
                    node2.name = node2.name + str(the_array.index(node2))
                    name_changed = True
                    any_name_changed = True
            if name_changed:
                node1.name = node1.name + str(the_array.index(node1))
        return any_name_changed
    def check_for_repeat_names(self):
        '''warning: this checks and fixes the repeat names of the graph's nodes and edges'''
        return (self._check_for_repeat_names(self.nodes) and self._check_for_repeat_names(self.arcs))
    @staticmethod
    def _make_unique_name(some_list):
        latest = 0
        for each in some_list:
            if some_list.name.isdigit():
                latest = some_list.name
        newest = str(int(latest)+1)
        return newest
    def make_unique_node_name(self):
        return self._make_unique_name(self.nodes)
    def make_unique_arc_name(self):
        return self._make_unique_name(self.arcs)
    def internally_connect_graph(self):
        raise NotImplementedError, bryan_message
    def last_node(self):
        return self.nodes[-1:]
    def last_arc(self):
        return self.arcs[-1:]
    def graphic(self):
        '''returns a list of the degrees of the nodes in the graph.'''
        return_value = []
        for current_node in self.nodes:
            return_value.append(current_node.degree())
        return return_value
    def max_degree(self):
        return max(self.graphic())
    #methods for properly linking nodes and arcs together
    def add_arc(self, arc_name="", from_node=None, to_node=None, arc=None):
        #first case: only arc is given
        if arc_name is None and from_node is None and to_node is None and arc is not None:
            self.arcs.append(arc)
            return
        #catch when arc_name is ""
        if arc_name == "": arc_name = self.make_unique_arc_name()
        #complain when we don't get anything
        if arc_name == "" and from_node is None and to_node is None:
            raise ValueError, "Graph.add_arc must be given at least one parameter."
        #construct a new arc
        temp = Arc(name=arc_name, from_node=from_node, to_node=to_node)
        self.arcs.append(temp)
        temp._from = from_node
        temp._to = to_node
        #self.last_arc()._from = from_node
        #self.last_arc()._to = to_node
        return temp
    def remove_arc(self, identifier):
        if isinstance(identifier, Arc):
            self.arcs.remove(identifier)
        elif isinstance(identifier, int):
            self.arcs.pop(identifier)
        else:
            raise IndexError, "Graph.remove_arc: identifier not in list."
        return
    def add_node(self, new_name="", node_ref=None):
        if node_ref is not None and new_name is not None:
            raise ValueError, "Graph.add_node: can't both add the node and make a node with the new name, do it yourself."
        if node_ref is not None:
            self.nodes.append(node_ref)
        if new_name == "": new_name = self.make_unique_node_name()
        temp = Node(name=new_name)
        self.nodes.append(temp)
        return temp
    def remove_node(self, node_ref=None, node_index=None, remove_arcs_too=False, remove_node_ref=True):
        '''removing a node is a little more complicated than removing arcs
        since we need to decide what to do with dangling arcs. As a result
        there are two booleans that specify how to handle the arcs.
        removeArcToo will simply delete the attached arcs if true, otherwise it
        will leave them dangling (default is false).
        removeNodeRef will change the references within the attached arcs to null
        if set to true, or will leave them if false (default is true).'''
        #some initial logic to deal with the given parameters
        if node_index is None and node_ref is None: raise ValueError, "Graph.remove_node: must be given either a node or a node_index"
        if node_index is not None:
            if node_index > len(self.nodes)-1: raise IndexError, "Graph.remove_node: node_index is bad."
            node_ref = self.nodes[node_index]
            
        if remove_arcs_too:
            for connected_arc in node_ref.arcs:
                self.remove_arc(connected_arc)
            self.nodes.remove(node_ref)
        elif remove_node_ref:
            for connected_arc in node_ref.arcs:
                if connected_arc._from == node_ref:
                    connected_arc._from = None
                else: connected_arc._to = None
            self.nodes.remove(node_ref)
        else: self.nodes.remove(node_ref)
    def save_gxml(file_path, version=2.0, mode="w"):
        assert not (mode=="w" and os.path.exists(file_path)), "Graph.save_gxml: file path (%s) already exists. try write mode (mode=w)?" % (file_path)
        assert version==2.0, "Graph.save_gxml: only able to save GraphSynth 2.0 gxml files (version=2.0)"
        
        #this is a terrible xml output method. don't try this at home kids :(
        output = ""
        output = output + '<Page xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" xmlns:GraphSynth="ignorableUri" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="GraphSynth" Tag="Graph">' + '\n'
        output = output + '<GraphSynth:designGraph xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">' + '\n'
        
        #global labels
        if len(self.global_labels) == 0: output = output + '<globalLabels />\n'
        else:
            output = output + '<globalLabels>' + '\n'
            for label in self.global_labels:
                output = output + '<globalLabel>' + label + '</globalLabel>' + '\n'
            output = output + '</globalLabels>' + '\n'

        #global variables
        if len(self.global_variables) == 0: output = output + '<globalVariables />\n'
        else:
            output = output + '<globalVariables>' + '\n'
            for var in self.global_variables:
                output = output + '<globalVariable>' + var + '</globalVariable>' + '\n'
            output = output + '</globalVariables>' + '\n'

        #arcs
        if len(self.arcs) == 0: output = output + '<arcs />\n'
        else:
            output = output + '<arcs>' + '\n'
            for arc in self.arcs:
                output = output + arc.to_gxml()
            output = output + '</arcs>' + '\n'

        #nodes
        if len(self.nodes) == 0: output = output + '<nodes />\n'
        else:
            output = output + '<nodes>' + '\n'
            for node in self.nodes:
                output = output + node.to_gxml()
            output = output + '</nodes>' + '\n'

        output = output + '</GraphSynth:designGraph>' + '\n'
        output = output + '</Page>'

        #save output
        fh = open(file_path, mode)
        fh.write(output)
        fh.close()

        return output #just because we're friendly

    @staticmethod
    def load_gxml(file_path, version=2.0, debug=False):
        '''input: gxml file path
        output: new Graph object'''
        #check that the path exists
        assert os.path.exists(file_path), "Graph.load_gxml: file path (%s) must exist." % (file_path)
        if debug: print "warning: canvas graphics will not be loaded"

        #open it up
        doc = minidom.parse(open(file_path, "r"))

        if version==2.0:
            result = Graph()
            result.filename = file_path

            page = doc.getElementsByTagName("Page")[0]
            #print (page.getElementsByTagName("name")[0].childNodes[0].data)
            #page_name = page.getElementsByTagName("name")[0].wholeText #name of the entire file (sort of)
            #page_name = page.getElementsByTagName("name")[0].childNodes[0].data
            page_name = os.path.basename(file_path)
            graph = page.getElementsByTagName("GraphSynth:designGraph")[0] #assume there is only one graph present

            graphics = page.getElementsByTagName("GraphSynth:Canvas")[0]

            #set up the variables for the for loop
            graph_name, global_labels, global_variables, arcs, nodes = None, [], [], [], []
            for child in graph.childNodes:
                if child.nodeName == "name":
                    graph_name = child.childNodes[0].wholeText
                elif child.nodeName == "globalLabels":
                    global_labels = child
                elif child.nodeName == "globalVariables":
                    global_variables = child
                elif child.nodeName == "arcs":
                    arcs = child
                elif child.nodeName == "nodes":
                    nodes = child
            #now process the results
            if len(global_labels.childNodes) > 0: print "TODO: implement global_labels for graphs" #TODO
            if len(global_variables.childNodes) > 0: print "TODO: implement global_variables for graphs" #TODO
            for global_label in global_labels.childNodes:
                #process each label
                result.global_labels.append(global_label)
            for global_variable in global_variables.childNodes:
                #process each variable
                result.global_variables.append(global_variable)
            
            #read in the nodes first
            for node in nodes.childNodes:
                name, local_labels, local_variables, x, y, z = "", [], [], 0, 0, 0
                for child in node.childNodes:
                    if child.nodeName == "name": name = child.childNodes[0].data
                    elif child.nodeName == "localLabels":
                        ll_xml = child
                        for label_xml in ll_xml.childNodes:
                            if len(label_xml.childNodes) > 0:
                                local_labels.append(label_xml.childNodes[0].data)
                    elif child.nodeName == "localVariables":
                        lv_xml = child
                        for variable_xml in lv_xml.childNodes:
                            if len(variable_xml.childNodes) > 0:
                                local_variables.append(variable_xml.childNodes[0].data)
                    elif child.nodeName == "X": x = child.childNodes[0].data
                    elif child.nodeName == "Y": y = child.childNodes[0].data
                    elif child.nodeName == "Z": z = child.childNodes[0].data

                #for some reason there's a lot of crap in the xml file?
                #nodes with blank names?? but i don't see any when i look
                if name == "\n    " or name == "": continue

                new_node = Node(name)
                new_node.local_labels = local_labels
                new_node.local_variables = local_variables
                new_node.x, new_node.y, new_node.z = x, y, z
                result.nodes.append(new_node)
            
            #arcs are done after the nodes so the references can be used
            for arc in arcs.childNodes:
                name, local_labels, local_variables, directed, doubly_directed, _from, _to = "", [], [], False, False, None, None
                for child in arc.childNodes:
                    if child.nodeName == "name":
                        name = child.childNodes[0].data
                    elif child.nodeName == "localLabels":
                        ll_xml = child
                        for label_xml in ll_xml.childNodes:
                            if len(label_xml.childNodes) > 0:
                                local_labels.append(label_xml.childNodes[0].data)
                    elif child.nodeName == "localVariables":
                        lv_xml = child
                        for variable_xml in lv_xml.childNodes:
                            if len(variable_xml.childNodes) > 0:
                                local_variables.append(variable_xml.childNodes[0].data)
                    elif child.nodeName == "directed":
                        if len(child.childNodes) > 0:
                            val = child.childNodes[0].data
                            if val == "true": directed = True
                            elif val == "false": directed = False
                            else: print "GraphSynth.load_gxml: unknown value for 'directed' on an arc: ", val
                    elif child.nodeName == "doublyDirected":
                        if len(child.childNodes) > 0:
                            val = child.childNodes[0].data
                            if val == "true": doubly_directed = True
                            elif val == "false": doubly_directed = False
                            else: print "GraphSynth.load_gxml: unknown value for 'doublyDirected' on an arc: ", val
                    elif child.nodeName == "From" or child.nodeName == "To":
                        if len(child.childNodes) > 0:
                            node_name = child.childNodes[0].data
                            if node_name == "": continue #ok we're fine with a dangling arc
                            the_node = None
                            
                            #now find the node in the current list
                            for node in result.nodes:
                                if node.name == node_name:
                                    the_node = node
                                    break
                            if the_node == None: raise ValueError, "GraphSynth.load_gxml: arc points to an imaginary node (it's not just dangling)"

                            if child.nodeName.lower() == "from": _from = [the_node]
                            elif child.nodeName.lower() == "to": _to = [the_node]

                if name == "": continue #this arc doesn't have a node name. this probably an xml data artifact

                new_arc = Arc(name)
                new_arc.directed = directed
                new_arc.doubly_directed = doubly_directed
                new_arc.local_labels = local_labels
                new_arc.local_variables = local_variables
                new_arc._from = _from
                new_arc._to = _to
                result.arcs.append(new_arc)
            
            result.name = graph_name
            result.page_name = page_name
            
            #TODO: append global variables, global labels into the graph
        return result

class Candidate:
    graphsynth_path = "GraphSynth.Representation/BasicGraphClasses/candidate.cs"
    #just for my reference
    previous_states = [] #a list of Graph objects
    current_state = None #a Graph
    age = -1 #the number of iterations this graph has gone through (set by the search process)

    def __init__(self, graph=None, previous_states=[], current_state=None, recipe=[], performance_params=[], active_rule_set=-1, age=-1, generation_status=[]):
        self._graph = graph
        self.previous_states = previous_states
        self.current_state = current_state
        self.recipe = recipe
        self.performance_params = performance_params
        self.active_rule_set = active_rule_set
        self.age = age
        self.generation_status = generation_status
    def graph(self, some_other_graph):
        self.previous_states.append(self.graph)
        self.graph = some_other_graph
    def num_rules_called(self):
        return len(self.recipe)
    def last_rule_set_index(self):
        return self.recipe[len(self.recipe) - 1].ruleset_index
    def rule_numbers_in_recipe(self):
        return set(self.recipe)
    def rule_set_indices_in_recipe(self):
        indices = []
        for rule in self.recipe:
            indices.append(rule.ruleset_index)
        return set(indices)
    def option_numbers_in_recipe(self):
        options = []
        for rule in self.recipe:
            options.append(rule.option_number)
        return set(options)
    def parameters_in_recipe(self):
        params = []
        for rule in self.recipe:
            params.extend(rule.parameters)
        return params
    def save_current(self):
        if self.current_state:
            self.prev_states.append(copy(self))
    def add_to_recipe(self, rule_option):
        self.recipe.append(deepcopy(rule_option)) #use deepcopy because we cant predict the future of a search algorithm
    def undo_last_rule(self):
        assert len(self.prev_states)>0, "Candidate.undo_last_rule: requires a previous state to revert back to."
        self.active_rule_set_index = self.last_rule_set_index
        self.current_state = self.prev_states[-1:]
        self.prev_states.remove(self.prev_states[-1:])
        self.recipe.pop(len(self.recipe)-1) #or self.recipe.remove(self.recipe[-1:]
        self.performance_params = [] #TODO: should the size of this list be preserved?
    def save_to_xml(self, filename=None):
        '''exports this graph into the graphsynth gxml format'''
        assert NotImplementedError, bryan_message
    def save_to_yaml(self, filename=None):
        '''not guaranteed to be pretty'''
        assert NotImplementedError, "Candidate.save_to_yaml: " + bryan_message
        handler = open(filename, 'w')
        handler.write(yaml.dump(self, default_flow_style=False))
        handler.close()

class Rule: #GrammarRule
    base_path = "GraphSynth.Representation/RuleClasses/"
    graphsynth_path = [base_path + "grammarRule.Basic.cs", base_path + "grammarRule.RecognizeApply.cs", base_path + "grammarRule.ShapeMethods.cs"]
    name = ""
    spanning = False
    induced = False
    negate_labels = []
    contains_all_global_labels = False
    ordered_global_labels = False
    embedding_rules = [] #a list of EmbeddingRule objects
    recognize_functions = []
    recognize_funcs = []
    apply_functions = []
    apply_funcs = []
    DLLofFunctions = None
    locations = [] #list of Graph objects
    L = None #Graph
    R = None #Graph

    def no_other_arcs_in_host(self, host_graph, located_nodes, located_arcs):
        '''are there any arcs in the host between recognized nodes?'''
        #check each arc of the host
        #if the arc is not in located nodes but connects two located in nodes then return false
        for arc in host_graph.arcs:
            if not (arc in located_arcs) and arc._from in located_nodes and arc._to in located_nodes:
                return False
        #if the check makes it through all arcs, return true
        return True
    def labels_match(self, host_labels=[]):
        if self.ordered_global_labels: return self.order_labels_match(host_labels)
        else: return self.unordered_labels_match(host_labels)
    def order_labels_match(self, host_labels=[]):
        any_found = False
        found = True
        #first an easy check to see if any negating labels exist in host_labels
        #if so, return false
        for label in self.negate_labels:
            if label in host_labels: return False
        for label in host_labels:
            if not (host_labels.index(label) == self.L.global_labels.index(label)):
                found = False
                break
        if found:
            loc = Graph()
            any_found = True
            #TODO: confirm if this is right (see grammarRule.Basic.cs line 137)
            loc.global_labels.extend(host_labels)
            self.locations.append(loc)
        return any_found
    def unordered_labels_match(self, host_labels=[]):
        for label in self.negate_labels:
            if label in host_labels: return False
        #note: you may have multiple identical labels
        temp_labels = copy(host_labels)
        for label in self.L.global_labels:
            if label in temp_labels:
                temp_labels.remove(label)
            else: return False
        #if there are no more temp_labels, then the two match up completely
        #else return false
        if self.contains_all_global_labels and not len(temp_labels)==0: return False
        return True
    @staticmethod
    def _make_unique_name(some_list, other_list):
        '''generates a unique name based off of the contents in some_list and other_list'''
        total_set = set()
        for x in [some_list, other_list]:
            for each in x:
                if some_list.name.isdigit():
                    total_set.add(name)
        return str(int(list(total_set).pop()) + 1)
    def make_unique_node_name(self):
        return Rule._make_unique_name(self.L.nodes, self.R.nodes)
    def make_unique_arc_name(self):
        return Rule._make_unique_name(self.L.nodes, self.R.arcs)
    def recognize(self, host, transform_matrices=[]):
        '''here is the big one! Although it looks compact, a lot of time can be spent in 
        the recursion that it invokes. Before we get to that, we wanna make sure that 
        our time there is well spent. As a result, we try to rule out whether the rule
        can even be applied at first -- hence the series of nested if-thens. If you don't
        meet the first, leave now! likewise for the second. The third is a little trickier.
        if there are no nodes or arcs in this rule, then it has already proven to be valid
        by the global labels - thus return a single location labeled "anywhere".
        if there are no nodes in the rule, then jump to the special function recognizeInitialArcInHost
        finally, if the node with the highest degree is higher than the highest degree
        of the host, then no need to recurse any further. Else, get into recognizeInitialNodeInHost,  
        which further calls recognizeRecursion.'''
        self.locations = []
        if self.labels_match(host.global_labels):
            if not self.spanning or self.spanning and (len(self.L.nodes) == len(host.nodes)):
                if len(self.L.nodes)==0 and len(self.L.arcs)==0: self.locations.append(Graph())
                elif len(self.L.nodes)==0: self.recognize_initial_arc_in_host(host)
                elif self.L.max_degree() < host.max_degree(): self.recognize_initial_node_in_host(host)
        i = 0
        length = len(self.locations) #we dont have to do -1 because while is < and not <=
        while i < length:
            location = self.locations[i]
            T = self.find_transform(location.nodes)
            if not self.use_shape_restrictions or (self.valid_transform(T) and self.other_nodes_comply(T, location.nodes)):
                transform_matrices.append(T)
                i+=1
            else: locations.pop(i)
        return locations
    def recognize_initial_node_in_host(self, host):
        starting_L_node = self.L.nodes[0]
        #if the first node of L (L.nodes[0]) is not in the host, then we can stop
        #as a rule of thumb, the creator of the grammar rules should always put the
        #most restrictive node FIRST in L, this will allow for a more efficient recognize routine.
        for current_host_node in host.nodes:
            #see if it matches with each node in host
            if starting_L_node.match_with(current_host_node):
                '''we will be storing potential locations in these two lists.
                it will be necessary to keep making copies of these lists as
                we discover new potential subgraphs. So, I wanna make sure these
                are as light as possible. Instead of making a whole designGraph
                instance, we will just move around these 2 lists. The lists will
                point to the actual elements in host, but will correspond in size 
                and position to those in 'this' L. Since we know the size ahead
                of time, we can preset the 'capacity' of the list. however this doesn't
                mean the lists are actually that size, so we need to explicitly
                initialize the lists.'''
                located_nodes = []
                located_arcs = []
                for i in range(len(self.L.nodes)):
                    located_nodes.append(None)
                for i in range(len(self.L.arcs)):
                    located_arcs.append(None)
                located_nodes[0] = current_host_node
                #we've made one match so set that up before invoking the recursion
                self.recognize_recursion(host, located_nodes, located_arcs, starting_L_node, current_host_node)
    def recognize_initial_arc_in_host(self, host):
        starting_L_arc = self.L.arcs[0]
        for current_host_arc in host.arcs:
            if starting_L_arc.match_with(current_host_arc):
                located_nodes = []
                located_arcs = []
                for i in range(len(self.L.nodes)):
                    located_nodes.append(None)
                for i in range(len(self.L.arcs)):
                    located_arcs.append(None)
                located_arcs[0] = current_host_arc
                self.recognize_recursion(host, located_nodes, located_arcs, None, None) #ok positional args really do suck
    def recognize_recursion(self, located_nodes, located_arcs, from_L_node, from_host_node):
        '''Here is the main recursive function. Based on the current conditions within the recursion
        one of four cases maybe invoked.
        1. (case1LocationFound) All nodes and arcs within locatedNodes and locatedArcs have been
           filled with pointers to nodes and arcs in the host. If this is the case, then we can add
           the location. however, you will need to check the enigmatic INDUCED condition.
        '''
        if not None in located_nodes and not None in located_arcs: self.case_1_location_found(host, located_nodes, located_arcs)
        else:
            '''
            the last thing the recursion did was find a new node to start from.
            see if there are any valid arcs on the L that still need to be matched with
            the host. Here, currentLArcIndex is used instead of the actual reference
            to the L arc. Why? Because, the index is useful both to the L and to locatedArcs
            which lists arcs in the same way as they appear in the L.
            '''
            current_L_arc_index = -1
            traverse_forward = False
            #this odd little boolean is used to indicate whether or not we are following the
            #arc in the proper direction regardless of the direction. We want to be able to follow
            #arcs backwards for recognition sake, so this is only useful in the eventual matchWith
            #method if direction is important.
            for the_arc in self.L.arcs:
                #this for loop seeks a L node leaving our fromLNode. If there is more than one arc, than
                #the loop may re-write currentLArcIndex and traverseForward. That's okay. Because we only
                #want one at this point. The recursion will eventually come around to any others that may
                #be skipped over here.
                i = self.L.arcs.index(the_arc)
                if the_arc._from == from_L_node and located_arcs[i]==None:
                    current_L_arc_index = i
                    traverse_forward = True
                elif the_arc._to == from_L_node and located_arcs[i]==None:
                    current_L_arc_index = i
                    traverse_forward = False
            if current_l_arc_index == -1:
                #2. (case2FindNewFromNode) if you get here, then it means that then were no more arcs
                #   leaving the last node. Unfortunately, since Case 1 was not met, there are still
                #   openings in the locations - either arcs and/or nodes.
                self.case_2_find_new_from_node(host, located_nodes, located_arcs, from_L_nodes)
            else:
                #so, currentLArcIndex now, points to a LArc that has yet to be recognized. What we do from
                #this point depends on whether that LArc points to an L node we have yet to recognize, an L
                #node we have recognized, or null.
                next_L_node = self.L.arcs[current_L_arc_index].other_node(from_L_node)
                if next_L_node is None:
                    #3. (case3DanglingNodes) If nextLNode is null then we need to simply find a match for
                    #the arc indicated by currentLArcIndex. Similar to case2, this function will need to
                    #find a new starting point in matching the graphs.
                    self.case_3_dangling_L_node(host, located_nodes, located_arcs, from_L_node, from_host_node, current_L_arc_index, traverse_forward)
                elif located_nodes[self.L.nodes.index(next_L_node)] is not None:
                    #4. (case4ConnectingBackToPrevRecNode) So, a proper arc was found leaving the
                    #   last L node. Problem is, it points back to a node that we've already located.
                    #   That means that we also already found what host node it connects to.
                    self.case_4_connecting_back_to_prev_rec_node(host, located_nodes, located_arcs, next_L_node, from_host_node, current_L_arc_index, traverse_forward)
                else:
                    #5. (case5FindingNewNodes) Okay, so nothing strange here. You are following an arc
                    #   that is leading to a yet undiscovered node. Good luck!
                    self.case_5_finding_new_nodes(host, located_nodes, located_arcs, next_L_node, from_host_node, current_L_arc_index, traverse_forward)
    def case1_location_found(self, host, located_nodes, located_arcs):
        '''a complete subgraph has been found. However, there is two more conditions to check.
        The induced boolean indicates that if there are any arcs in the host between the
        nodes of the subgraph that are not in L then this is not a valid location. After this we
        check the variables for a violation.
        '''
        param_functions_violated=False
        if not self.induced or (self.induced and self.no_other_arcs_in_host(host, located_nodes, located_arcs)):
            recognize_arguments = [self.L, host, located_nodes, located_arcs]
            #FIXME dll stuff omitted (!) -- probably very important?
            for recognize_function in self.recognize_funcs:
                if recognize_function(recognize_arguments):
                    param_functions_violated = True
                    break
            if not param_functions_violated: self.locations.append(Graph(located_nodes, located_arcs))
    def case2_find_new_from_node(self, host, located_nodes, located_arcs):
        next_L_node_index = self.L.nodes.index(from_L_node) + 1
        if len(self.L.nodes) == next_L_node_index:
            next_L_node_index = 0 #these 3 prev.lines simply go to the next node in L
                                  # - if you're at the end then wraparound to 0.
        next_L_node = self.L.nodes[next_L_node_index]
        if located_nodes[next_L_node_index] == None:
            #this acts like a mini-recognizeInitialNodeInHost function, we are forced to jump to a new starting
            #point in L - careful, though, that we don't check it with a node that has already been included
            #as part of the location.
            for current_host_node in host.nodes:
                if not (current_host_node in located_nodes) and next_L_node.match_with(current_host_node):
                    new_located_nodes = [] #copy the locatedNodes to a new list.
                                           #just in case the above foreach statement
                                           #find several matches for our new
                                           #starting node - we wouldnt want to alter
                                           #locatedNodes to affect that but rather
                                           #merely to re-invoke the recusion.
                    for i in range(len(located_nodes)):
                        new_located_nodes.append(None)
                    new_located_nodes[next_L_node_index] = current_host_node
                    self.recognize_recursion(host, new_located_nodes, located_arcs, next_L_node, current_host_node)
        #so the next L node has already been recognized. Well, then we can restart the recursion as if we are
        #coming from this node. It's possible that recognizeRecursion will just throw you back into this function
        #but that's okay. we just advance to the next node and look for new 'openings'.
        else: recognize_recursion(host, located_nodes, located_arcs, next_L_node, located_nodes[next_L_node_index])
    def case3_dangling_nodes(self, host, located_nodes, located_arcs, from_L_node, from_host_node, current_L_arc_index, traverse_forward):
        current_L_arc = self.L.arcs[current_L_arc_index] #first we must match the arc to a possible arc
                                                         #leaving the from_host_node
        next_host_node = None
        neighbor_host_arcs = []
        for each in host.arcs: #FIXME this used to be a "delegate" call of some sort?
            if (each in located_arcs) and current_L_arc.match_with(each, from_host_node, traverse_forward):
                neighbor_host_arcs.append(each)
        if len(neighbor_host_arcs) > 0: #if there are no recognized arcs we just leave
            for host_arc in neighbor_host_arcs:
                #for each arc that was recognized, we now need to check that the destination node matches.
                next_host_node = host_arc.other_node(from_host_node)
                if not current_L_arc.null_means_null or next_host_node is None:
                    #if nullMeansNull is false than ANY host node is fine even if its also null. If nullMeansNull
                    #is true, however, than we need to make sure fromHostNode is also null.
                    new_located_arcs = []
                    for i in range(current_L_arc_index):
                        new_located_arcs.append(None)
                    new_located_arcs[current_L_arc_index] = host_arc
                    #re-invoking the recursion is "tough" from this point. since we just hit a dead end in L.
                    #the best thing to do is just use the very same fromLnode and fromHostNode that were
                    #used in the previous recognizeRecursion.
                    self.recognize_recursion(host, located_nodes, new_located_arcs, from_L_node, from_host_node)
    def case4_connecting_back_to_prev_rec_node(self, host, located_nodes, located_arcs, next_L_node, from_host_node, current_L_arc_index, traverse_forward):
        current_L_arc = self.L.arcs[current_L_arc_index] #first we must match the arc to a possible arc
                                                         #leaving the from_host_node
        next_host_node = located_nodes[self.L.nodes.index(next_L_node)]
        neighbor_host_arcs = []
        for some_arc in host.arcs: #there may be several possible arcs that match with current_L_arc so we make a list called neighbor_host_arcs
            if not (some_arc in located_arcs) and current_L_arc.match_with(some_arc, from_host_node, next_host_node, traverse_forward):
                neighbor_host_arcs.append(some_arc)
        if len(neighbor_host_arcs) > 0: #if there are no recognized arcs we just leave
            for host_arc in neighbor_host_arcs:
                new_located_nodes = []
                new_located_nodes[L.nodes.index(next_L_node)] = next_host_node #FIXME was a 'delegate' in the original graphsynth source
                new_located_arcs[current_L_arc_index] = host_arc
                self.recognize_recursion(host, new_located_nodes, new_located_arcs, next_L_node, next_host_node)
    def case5_finding_new_nodes(self, host, located_nodes, located_arcs, next_L_node, from_host_node, current_L_arc_index, traverse_forward):
        #this function starts very similar to Case 4. It is, however, more comlex since we need to match
        #the next node in L to a node in the host. The function begin the same as above by gathering the
        #potential arcs leaving the host and checking them for compatibility.
        current_L_arc = self.L.arcs[current_L_arc_index]
        next_host_node = None
        for each in host.arcs:
            if (not each in located_arcs) and current_L_arc.match_with(each, from_host_node, traverse_forward):
                neighbor_host_arcs.append(each)
        if len(neighbor_host_arcs) > 0:
            for host_arc in neighbor_host_arcs:
                #for each arc that was recognized, we now need to check that the destination node matches.
                next_host_node = host_arc.other_node(from_host_node)
                if next_L_node.match_with(next_host_node) and not (next_host_node in located_nodes):
                    #if the nodes match than we can update locations and re-invoke the recursion. It is important
                    #to copy the locatedNodes to a new list, just in case the above foreach statement finds
                    #several matches for our new new L node.
                    new_located_nodes = copy(located_nodes)
                    for i in range(len(self.L.nodes)):
                        new_located_nodes.append(None)
                    for a in self.L.nodes:
                        if a == next_L_node:
                            new_located_nodes[self.L.nodes.index(a)] = next_host_node
                    new_located_arcs = copy(located_arcs)
                    new_located_arcs[current_L_arc_index] = host_arc
                    self.recognize_recursion(host, new_located_nodes, new_located_arcs, next_L_node, next_host_node)
    def apply(self, L_mapping, host, position_t, parameters=[]):
        for a in self.L.global_labels:
            if not self.R.contains(a):
                host.global_labels.remove(a) #removing the lables in L but not in R
        #if there are multiple identical R.global_labels, they are not added
        for a in self.R.global_labels:
            if not self.R.contains(a):
                host.global_lables.append(a) #and adding the label in R but not in L
        #do the same now, for the variables.
        for a in self.L.global_variables:
            if not self.R.global_variables.contains(a):
                host.global_variables.remove(a) #removing the variables in L but not in R
        for a in self.R.global_variables:
            if not self.L.global_variables.contains(a):
                host.global_variables.append(a) #and adding the variables in R but not in L
        
        #First set up the Rmapping, which is a list of nodes within the host
        #that corresponds in length and position to the nodes in R, just as
        #Lmapping contains lists of nodes and arcs in the order they are
        #referred to in L.
        R_mapping = Graph()
        #we do not know what these will point to yet, so just
        #make it of proper length at this point.
        #DEBUG HINT: you should check R_mapping at the end of
        #the function - it should contain no None values.
        for node in self.R.nodes:
            R_mapping.nodes.append(None)
        for arc in self.R.arcs:
            R_mapping.arcs.append(None)
        self.remove_L_diff_K_from_host(L_mapping, host)
        self.add_R_diff_K_to_D(L_mapping, R_mapping, position_T) 
        '''these two lines correspond to the two "pushouts" of the double pushout algorithm.
             L <--- K ---> R     this is from freeArc embedding (aka edNCE)
             |      |      |        |      this is from the parametric update
             |      |      |        |       |
           host <-- D ---> H1 ---> H2 ---> H3
         The first step is to create D by removing the part of L not found in K (the commonality).
         Second, we add the elements of R not found in K to D to create the updated host, H. Note,  
         that in order to do this, we must know what subgraph of the host we are manipulating - this
         is the location mapping found by the recognize function.'''
        self.free_arc_embedding(L_mapping, host, R_mapping)
        #however, there may still be a need to embed the graph with other arcs left dangling,
        #as in the "edge directed Node Controlled Embedding approach", which considers the neighbor-
        #hood of nodes and arcs of the recognized Lmapping.
        self.update_parameters(L_mapping, host, R_mapping, parameters)
    def remove_L_diff_K_from_host(self, L_mapping, host):
        '''foreach node in L - see if it "is" also in R - if it is in R than it "is" part of the
        commonality subgraph K, and thus should not be deleted as it is part of the connectivity
        information for applying the rule. Note that what we mean by "is" is that there is a
        node with the same name. The name tag in a node is not superficial - it contains
        useful connectivity information. We use it as a stand in for referencing the same object
        this is different than the local lables which are used for recognition and the storage
        any important design information.
        '''
        for some_node in self.L.nodes:
            i = self.L.nodes.index(some_node)
            exists = False
            for node in self.R.nodes:
                if node.name == self.L.node.name:
                    exists = True
                    break
            #if a node with the same name does not exist in R, then it is safe to remove it.
            #The removeNode should is invoked with the "false false" switches of this function.
            #This causes the arcs to be unaffected by the deletion of a connecting node. Why
            #do this? It is important in the edNCE approach that is appended to the DPO approach
            #(see the function freeArcEmbedding) in connecting up a new R to the elements of L
            #a node was connected to.
            if not exists: host.remove_node(L_mapping.nodes[i], False, False)
        for some_arc in self.L.arcs:
            i = self.L.arcs.index(some_arc)
            exists = False
            for arc in self.R.arcs:
                if some_arc.name == arc.name:
                    exists=True
                    break
            if not exists: host.remove_arc(L_mapping.arcs[i])
    def add_R_diff_K_to_D(self, L_mapping, D, R_mapping, position_T):
        '''in this adding and gluing function, we are careful to distinguish
        the Lmapping or recognized subgraph of L in the host - heretofore
        known as Lmapping - from the mapping of new nodes and arcs of the
        graph, which we call Rmapping. This is a complex function that goes
        through 4 key steps:
        1. add the new nodes that are in R but not in L.
        2. update the remaining nodes common to L&R (aka K nodes) that might
           have had some label changes.
        3. add the new arcs that are in R but not in L. These may connect to
           either the newly connected nodes from step 1 or from the updated nodes
           of step 2.
        4. update the arcs common to L&R (aka K arcs) which might now be connected
           to new nodes created in step 1 (they are already connected to 
           nodes in K). Also make sure to update their labels just as K nodes were
           updated in step 2.'''
        #here are some placeholders used in this bookeeping. Many are used multiple times
        #so we might as well declare them just once at the start.
        index1, index2, from_node, to_node, k_node, k_arc = None, None, None, None, None, None
        for r_node in self.R.nodes:
            #step 1. add new nodes to D
            exists = False
            for each in self.L.nodes:
                if each.name == r_node.name:
                    exists=True
                    break
            if not exists:
                D.add_node(r_node.node_type) #create a new node #FIXME do "node_type" the python way
                R_mapping.nodes[i] = D.last_node #make sure it's referenced in R_mapping
                #labels cannot be set equal, since that merely sets the reference of this list
                #to the same value. So, we need to make a complete copy.
                r_node = copy(D.last_node) #FIXME: should this be deepcopy?
                #give that new node a name and labels to match with the R.
                self.update_position_of_node(D.last_node, position_T, r_node)
            #step 2. update K nodes.
            else:
                #else, we may need to modify or update the node. In the pure graph
                #grammar sense this is merely changing the local labels. In a way,
                #this is a like a set grammar. We need to find the labels in L that
                #are no longer in R and delete them, and we need to add the new labels
                #that are in R but not already in L. The ones common to both are left
                #alone.
                index1 = None
                for each in self.L.nodes: #find index of the common node in L
                    if each.name == r_node.name:
                        index1 = self.L.nodes.index(each)
                k_node = L_mapping.nodes[index1] #... and then set k_node to the actual node in D.
                R_mapping.nodes[i] = k_node #also, make sure that the R_mapping is the same node
                for a in self.L.nodes[index1].local_labels:
                    if not (a in r_node.local_labels): k_node.local_labels.remove(a) #removing the labels in L but not in R...
                for a in r_node.local_labels:
                    if not (a in self.L.nodes[index1].local_labels): k_node.local_labels.append(a) #...and adding the label in R but not in L.
                for a in self.L.nodes[index1].local_variables:
                    if not (a in r_node.local_variables): k_node.local_variables.remove(a) #removing the variables in L but not in R
                for a in r_node.local_variables:
                    if not (a in self.L.nodes[index1].local_variables): k_node.local_variables.append(a) #and adding the variable in R but not in L
                k_node.display_shape = copy(r_node.display_shape)
                self.update_position_of_node(k_node, position_T, r_node)
        #now moving onto the arcs (a little more challenging actually)
        for r_arc in self.R.arcs:
            i = self.R.arcs.index(r_arc)
            #step 3. add new arcs to D
            exists = False
            for test_arc in self.L.arcs:
                if test_arc.name == r_arc.name:
                    exists=True
                    break
            if not exists:
                #setting up where the arc comes from
                if r_arc._from == None: From = None
                else: #this should be reworked into an elif to be honest
                    #if the arc is coming from a node that is in K, then it must've been
                    #part of the location (or L_mapping) that was originally recognized.
                    exist1 = False
                    for ea in self.L.nodes:
                        if ea.name == r_arc._from.name:
                            exist1 = True
                            index1 = self.L.nodes.index(ea)
                            From = L_mapping.nodes[index1]
                            break
                    if not exist1:
                        #if not in K then the arc connects to one of the new nodes that were
                        #created at the beginning of this function (see step 1) and is now
                        #one of the references in R_mapping.
                        index1 = self.R.find_index_of_node_with(name=r_arc._from.name)
                        From = R_mapping.nodes[index1]
                #setting up where the arc goes
                #this code is the same of "setting up where arc comes from - except here
                #we do the same for the to connection of the arc.
                if r_arc._to is None: To = None
                else:
                    index1 = self.L.find_index_of_node_with(name=r_arc._to.name)
                    if index1 is not None and index1 is not False:
                        To = L_mapping.nodes[index1]
                    else:
                        index1 = self.R.find_index_of_node_with(name=r_arc._to.name)
                        To = R_mapping.nodes[index1]
                D.add_arc(r_arc.name, r_arc.arc_type, From, To)
                R_mapping.arcs[i] = D.last_arc
                r_arc.copy(D.last_arc)
            #step 4. update K arcs.
            else: #line 579 ish
                index2 = self.L.find_index_of_arc_with(name=r_arc.name)
                #first find the position of the same arc in L
                current_L_arc = self.L.arcs[index2]
                k_arc = L_mapping.arcs[index2] #then find the actual arc in D that is to be changed
                #one very subtle thing just happened here! (07/06/06) if the direction is reversed, then
                #you might mess-up this k_arc. We need to establish a boolean so that references
                #incorrectly altered.
                k_arc_is_reversed = False
                if not (L_mapping.nodes.index(k_arc._from) == self.L.nodes.index(current_L_arc._from)) and not (L_mapping.nodes.index(k_arc._to) == self.L.nodes.index(current_L_arc._to)):
                    k_arc_is_reversed = True
                R_mapping.arcs[i] = k_arc
                #similar to step 3. we first find how to update the from and to.
                if current_L_arc._from is not None and r_arc._from is None:
                    #this is a rare case in which you actually want to break an arc from its attached
                    #node. If the corresponding L arc is not null only! if it is null then it may be
                    #actually connected to something in the host, and we are in no place to remove it.
                    if k_arc_is_reversed: k_arc._to = None
                    else: k_arc._from = None
                elif r_arc._from is not None:
                    index1 = self.R.nodes.find_index_of_node_with(name=r_arc._from.name)
                    #find the position of node that this arc is supposed to connect to in R
                    if k_arc_is_reversed: k_arc._to = R_mapping.nodes[index1]
                    else: k_arc._from = R_mapping.nodes[index1]
                #now do the same for the To connection.
                if current_L_arc._to is not None and r_arc._to is None:
                    if k_arc_is_reversed: k_arc._from = None
                    else: k_arc._to = None
                elif r_arc._to is not None:
                    index1 = self.R.find_index_of_node_with(name=r_arc.To.name)
                    if k_arc_is_reversed: k_arc._from = R_mapping.nodes[index1]
                    else: k_arc._to = R_mapping.nodes[index1]
                #just like in step 2, we may need to update the labels of the arc.
                for a in current_L_arc.local_labels:
                    if not a in r_arc.local_labels: k_arc.local_labels.remove(a)
                for a in r_arc.local_labels:
                    if not a in current_L_arc.local_labels: k_arc.local_labels.append(a)
                for a in current_L_arc.local_variables:
                    if not a in r_arc.local_variables: k_arc.local_variables.remove(a)
                for a in r_arc.local_variables:
                    if not a in current_L_arc.local_variables: k_arc.local_variables.append(a)
                if (not k_arc.directed) or (k_arc.directed and current_L_arc.direction_is_equal):
                    k_arc.directed = r_arc.directed
                #if the k_arc is currently undirected or if it is and direction is equal
                #then the directed should be inherited from R.
                if (not k_arc.doubly_directed) or (k_arc.doubly_directed and current_L_arc.direction_is_equal):
                    k_arc.doubly_directed = r_arc.doubly_directed
                k_arc.display_shape = copy(r_arc.display_shape)
    def free_arc_embedding(self, L_mapping, host, R_mapping):
        '''There are nodes in host which may have been left dangling due to the fact that their 
        connected nodes were part of the L-R deletion. These now need to be either 1) connected
        up to their new nodes, 2) their references to old nodes need to be changed to null if 
        intentionally left dangling, or 3) the arcs are to be removed. In the function 
        removeLdiffKfromHost we remove old nodes but leave their references intact on their 
        connected arcs. This allows us to quickly find the list of freeArcs that are candidates 
        for the embedding rules. Essentially, we are capturing the neighborhood within the host 
        for the rule application, that is the arcs that are affected by the deletion of the L-R
        subgraph. Should one check non-dangling non-neighborhood arcs? No, this would seem to 
        cause a duplication of such an arc. Additionally, what node in host should the arc remain 
        attached to?  There seems to be no rigor in applying these more global (non-neighborhood) 
        changes within the literature as well for the general edNCE method.'''
        free_end_identifier = None
        new_node_to_connect, node_removed_in_L_diff_R_deletion, to_node, from_node = None, None, None, None
        neighbor_node = None
        num_of_arcs = len(host.arcs)

        for arc in host.arcs:
            #first, check to see if the arc is really a freeArc that needs updating.
            if self.embedding_rule.arc_is_free(arc, host, free_end_identifier, neighbor_node): #the last two are apparently return values? wtf FIXME
                free_arc = arc
                #For each of the embedding rules, we see if it is applicable to the identified freeArc.
                #The rule then modifies the arc by simply pointing it to the new node in R as indicated
                #by the embedding Rule's RNodeName. NOTE: the order of the rules are important. If two
                #rules are 'recognized' with the same freeArc only the first one will modify it, as it 
                #will then remove it from the freeArc list. This is useful in that rules may have precedence
                #to one another. There is an exception if the rule has allowArcDuplication set to true, 
                #since this would simply create a copy of the arc.
                for e_rule in self.embedding_rules: #FIXME where is embedding_rules defined? see line 683 in grammarRule.RecognizeApply.cs
                    new_node_to_connect = e_rule.find_new_node_to_connect(R, R_mapping)
                    node_removed_in_L_diff_R_deletion = e_rule.find_deleted_node(L, L_mapping)
                    if e_rule.rule_is_recognized(free_end_identifier, free_arc, neighbor_node, node_removed_in_L_diff_R_deletion):
                        #set up new connection points
                        if free_end_identifier >= 0:
                            if e_rule.new_direction >= 0:
                                to_node = new_node_to_connect
                                from_node = free_arc._from
                            else:
                                to_node = free_arc._from
                                from_node = new_node_to_connect
                    else:
                        if e_rule.new_direction <= 0:
                            from_node = new_node_to_connect
                            to_node = free_arc._to
                        else:
                            from_node = free_arc._to
                            to_node = new_node_to_connect
                    #if making a copy of arc, duplicate it and all the characteristics
                    if e_rule.allow_arc_duplication:
                        #under the allowArcDuplication section, we will be making a copy of the
                        #freeArc. This seems a little error-prone at first, since if there is only
                        #one rule that applies to freeArc then we will have good copy and the old
                        #bad copy. However, at the end of this function, we go through the arcs again
                        #and remove any arcs that still appear free. This also serves the purpose to
                        #delete any dangling nodes that were not recognized in any rules.
                        host.add_arc(copy(free_arc), from_node, to_node)
                    #else, just update the old free_arc
                    else:
                        free_arc._from = from_node
                        free_arc._to = to_node
                        break #skip the next arc
                        #this is done so that no more embedding rules will be checked with this free_arc
        #clean up (i.e. delete) any free_arcs that are still in host.arcs
        for arc in host.arcs:
            #this seems a little archaic to use this i-counter instead of foreach.
            #the issue is that since we are removing nodes from the list as we go
            #through it, we very well can't use foreach. The countdown allows us to
            #disregard problems with the deleting.
            #.. but this doesn't apply in python. :)
            if (arc._from is not None and arc._from not in host.nodes) or (arc._to is not None and arc._to not in host.nodes):
                host.remove_arc(arc)
    def update_parameters(self, L_mapping, host, R_mapping, parameters):
        apply_arguments = [L_mapping, host, R_mapping, parameters, self]
        #If you get an error in this function, it is most likely due to
        #an error in the compilted DLLofFunctions. Open your code for the
        #rules and leave this untouched - it's simply the messenger.
        #FIXME: omitted some DLLofFunctions stuff here
    #from grammarRule.ShapeMethods.cs
    epsilon = 0.000001
    regularization_matrix = []
    def reset_regularization_matrix(self):
        self.regularization_matrix = []
    def calculate_regularization_matrix(self):
        assert NotImplementedError, bryan_message_generator("GraphSynth.Representation/RuleClasses/grammarRule.ShapeMethods.cs")
    use_shape_restrictions = False
    transform_node_shapes = False
    translate, scale, skew, flip = None, None, None, None
    rotate, projection = None, None
    def find_transform(self, located_nodes):
        #if there are no nodes, simply return the identity matrix
        if len(located_nodes) == 0: return make_identity(3)
        x1, x2, x3, x4, y1, y2, y3, y4 = 0, 0, 0, 0, 0, 0, 0, 0
        tx, ty, wX, wY, a, b, c, d = 0, 0, 0, 0, 0, 0, 0, 0
        k1, k2, k3, k4 = 0, 0, 0, 0
        u3, u4, v3, v4 = 0, 0, 0, 0
        
        x1 = located_nodes[0].X
        y1 = located_nodes[0].Y
        if len(self.L.nodes) >= 2:
            x2 = located_nodes[1].X
            y2 = located_nodes[1].Y
        if len(self.L.nodes) >= 3:
            x3 = located_nodes[2].X
            y3 = located_nodes[2].Y
            temp = [self.L.nodes[2].X, self.L.nodes[2].Y, 1.0]
            temp = multiply(self.regularization_matrix, temp)
            u3 = temp[0] #this is going to be a whole row. is this right?
            u4 = temp[1] #FIXME
        if len(self.L.nodes) >= 4:
            x4 = located_nodes[3].X
            y4 = located_nodes[3].Y
            temp = [self.L.nodes[3].X, self.L.nodes[3].Y, 1.0]
            temp = multiply(self.regularization_matrix, temp)
            u4 = temp[0]
            v4 = temp[1]
        #set values for tx and ty
        tx = x1
        ty = y1
        #calculate projection terms
        if len(self.L.nodes) <= 3:
            wX, wY = 0, 0
        elif self.same_close_zero(v3 * v4):
            wX, wY = 0, 0
        else:
            #calculate intermediate values used only in this class or method
            k1 = u4 * v3 * (y4 - y2) - u3 * v4 * (y3 - y2)
            if same_close_zero(k1): k1 = 0
            else: k1 /= v3 * v4
            
            k2 = v4 * (y3 - y2 * u3 + ty * u3 - ty) + v3 * (-y4 - ty * u4 + y2 * u4 + ty)
            if same_close_zero(k2): k2 = 0
            else: k2 /= v3 * v4

            k3 = u3 * v4 * (x3 - x2) - u4 * v3 * (x4 - x2)
            if same_close_zero(k3): k3 = 0
            else: k3 /= v3 * v4

            k4 = v3 * (x4 - x2 * u4 + tx * u4 - tx) - v4 * (x3 + tx * u3 - x2 * u3 - tx)
            if same_close_zero(k4): k4 = 0
            else: k4 /= v3 * v4

            #calculate wY and wX
            wY = (k1 * k4) - (k2 * k3)
            if same_close_zero(wY): wY = 0
            else: wY /= k3 * (y3 - y4) + k1 * (x3 - x4) #equation 7

            wX = wY * (y3 - y4) + k2
            if same_close_zero(wX): wX = 0
            else: wX /= k1 #equation 8

        #region Calculate rotate, scale, skew terms
        if len(self.L.nodes) <= 1:
            a, d = 1, 1
            b, c = 0, 0
        else:
            #calculate a
            a = x2 * (wX + 1) - tx;
            #calculate c
            c = y2 * (wX + 1) - ty;

            if len(self.L.nodes) <= 2:
                """in order for the validTransform to function, b and d are set as
                if there is a rotation as opposed to a Skew in X. It is likely that
                isotropic transformations like rotation are more often intended than skews."""
                theta = math.atan2(-c, a)
                b = -c
                d = a
            else:
                #calculate b
                b = x3 * (wX * u3 + wY * v3 + 1) - a * u3 - tx
                if same_close_zero(b): b = 0
                else: b /= v3
                #calculate d
                d = y3 * (wX * u3 + wY * v3 + 1) - c * u3 - ty
                if same_close_zero(d): d = 0
                else: d /= v3
        T = [
            [a, b, tx], #row 0
            [c, d, ty], #row 1
            [wX, wY, 1] #row 3
            ]
        T = multiply(T, self.regularization_matrix)
        T[0][0] /= T[2][2]
        T[0][1] /= T[2][2]
        T[0][2] /= T[2][2]
        T[1][0] /= T[2][2]
        T[1][1] /= T[2][2]
        T[1][2] /= T[2][2]
        T[2][0] /= T[2][2]
        T[2][1] /= T[2][2]
        T[2][2] = 1
        return T
    def valid_transform(self, T, theta=None):
        '''in this function the candidate transform T "runs the gauntlet"
        the long set of if statements each return false, and if T makes it all
        the way through, we return true
        it's easy to check the translation and projection constraints first
        since there's a one-to-one match wtih variables in the matrix and the flags.'''
        if theta is not None: return self.valid_transform_theta(T, theta)
        if not same_close_zero(T[0][2]) and (self.translate == self.transform_type.only_x or self.translate == self.transform_type_prohibited):
            return False
        elif not same_close_zero(T[1][2]) and (self.translate == self.transform_type.only_x or self.translate == self.transform_type_prohibited):
            return False
        elif not same_close_zero(T[0][2], T[1][2]) and (self.translate == self.transform_type.only_x or self.translate == self.transform_type_prohibited):
            return False
        
        #now for projection
        if not same_close_zero(T[2][0]) and (self.projection == self.transform_type.only_x or self.projection == self.transform_type.prohibited):
            return False
        elif not same_close_zero(T[2][1]) and (self.projection == self.transform_type.only_x or self.projection == self.transform_type.prohibited):
            return False
        elif not same_close_zero(T[2][0], T[2][1]) and (self.projection == self.transform_type.only_x or self.projection == self.transform_type.prohibited):
            return False #FIXME (CHECKME)
        #Now, it's a little more complicated since the rotation occupies the same cells
        #in T as skewX, skewY, scaleX, and scaleY. The approach taken here is to solve
        #for theta (the amount of rotation) and then call/return what the overload produces
        #which requires theta and solves for skewX, skewY, scaleX, and scaleY.
        elif not self.rotate: return self.valid_transform(T, 0.0)
        #skew restrictions are easier than scale, because they default to (as in the identity matrix) 0 whereas scale is 1
        elif self.skew == self.transform_type.prohibited or self.skew == self.transform_type.only_y:
            return self.valid_transform(T, math.atan2(T[0][1], T[1][1]))
        elif self.skew == self.transform_type.only_x:
            return self.valid_transform(T, math.atan2(-T[1][0], T[0][0]))
        elif self.skew == self.transform_type.both_uniform:
            return self.valid_transform(T, math.atan2((T[0][1] - T[1][0]), (T[0][0] + T[1][1]))) #FIXME
        
        #Lastly, and most challenging, we look at Scale Restrictions. Flip is basically
        #the same and handled in the overload below.
        elif self.scale == self.transform_type.prohibited or self.scale == self.transform_type.only_y:
            #wtf are these variable names?
            TooPlusTio2 = T[0][0] * T[0][0] + T[1][0] * T[1][0]
            sqrtt2pt2 = math.sqrt(Too2PlusTio2)
            Ky = math.sqrt(Too2PlusTio2 - 1)
            return self.valid_transform(T, theta=math.acos(T[0][0] / sqrtt2pt2) + math.atan2(Ky, 1))
        elif self.scale == self.transform_type.only_y:
            Toi2PlusTii2 = T[0][1] * T[0][1] + T[1][1] * T[1][1]
            sqrtt2pt2 = math.sqrt(Toi2PlusTii2)
            Kx = math.sqrt(Toi2PlusTii2 - 1)
            return self.valid_transform(T, theta=math.acos(T[0][1] / sqrtt2pt2) + math.atan2(1, Kx))
        elif self.scale == self.transform_type.both_uniform: #FIXME
            return self.valid_transform(T, theta=math.atan2((T[0][0] - T[1][1]), (T[0][1] + T[1][0])))
    def valid_transform_theta(self, T, theta):
        #now with theta known, we can find the values for Sx, Sy, Kx, and Ky
        Kx = T[0][1] * math.cos(theta) - T[1][1] * math.sin(theta)
        Ky = T[0][0] * math.sin(theta) - T[1][0] * math.cos(theta)
        Sx = T[0][0] * math.cos(theta) - T[1][0] * math.sin(theta)
        Sy = T[0][1] * math.sin(theta) + T[1][1] * math.cos(theta)
        #now check the skew restrictions, once an error is found return false
        if same_close_zero(Kx) and ((self.skew == self.transform_type.prohibited) or (self.skew == self.transform_type.only_y)):
            return False
        elif not same_close_zero(Ky) and ((self.skew == self.transform_type.prohibited) or (self.skew == self.transform_type.only_y)):
            return False
        elif not same_close_zero(Kx, Ky) and self.skew == self.transform_type.both_uniform:
            return False
        #now we check scaling restrictions.
        elif not same_close_zero(math.abs(Sx), 1) and ((self.scale == self.transform_type.prohibited) or (self.scale == self.transform_type.only_y)):
            return False
        elif not same_close_zero(math.abs(Sy), 1) and ((self.scale == self.transform_type.prohibited) or (self.scale == self.transform_type.only_x)):
            return False
        elif not same_close_zero(math.abs(Sx), math.abs(Sy)) and self.scale == self.transform_type.both_uniform:
            return False
        #finally, we check if the shape has to be flipped
        if Sx<0 and ((self.flip == self.transform_type.prohibited) or (self.flip == self.transform_type.only_y)):
            return False
        if Sy<0 and ((self.flip == self.transform_type.prohibited) or (self.flip == self.transform_type.only_x)):
            return False
        if (Sx*Sy<0) and (self.flip == self.transform_type.both_uniform):
            return False
        else: return True
    def other_nodes_comply(self, T, located_nodes):
        if len(self.located_nodes) <= 3: return True
        else:
            i = 3
            while True:
                if i == len(self.located_nodes): break #FIXME does this go at the top or bottom of the while loop?
                vLVect = [self.L.nodes[i].X, self.L.nodes[i].Y, 1.0]
                vLVect = multiply(T, vLVect)
                vHostVect = [located_nodes[i].X, located_nodes[i].Y, 1.0]
                if (not same_close_zero(vLVect[0], vHostVect[0])) or (not same_close_zero(vLVect[1], vHostVect[1])):
                    return False
                i+=1
            return True
    def same_close_zero(self, x1, x2=None):
        if x2 is not None: return self.same_close_zero(x1 - x2)
        if math.abs(x1) < epsilon: return True
        else: return False
    def update_position_of_node(self, update, T, given): #given is a ruleNode
        pt = [given.X, given.Y, 1]
        pt = multiply(T, pt)
        newT = make_identity(3)
        newT[0][2] = update.X = pt[0] / pt[2]
        newT[1][2] = update.Y = pt[1] / pt[2]
        update.DisplayShape.transform_shape(newT)
    def update_shape_qualities_of_node(self, update, T, given):
        raise NotImplementedYet, campbell_message

#here we define additional qualities used only by arcs in the grammar rules.
#TODO: check if this is used anywhere
class RuleArc(Arc):
    graphsynth_path = "GraphSynth.Representation/RuleClasses/ruleArc.cs"
    def __init__(name="", all_local_labels=False, direction_is_equal=False, null_means_null=True, negate_labels=[]):
        self.name = name
        #The following booleans capture the possible ways in which an arc may/may not be a subset
        #(boolean set to false) or is equal (in this respective quality) to the host (boolean set
        #to true). These are special subset or equal booleans used by recognize. For this
        #fundamental arc classes, only these three possible conditions exist.
        self.contains_all_local_labels = all_local_labels
        #if true then all the localLabels in the lArc match with those in the host arc, if false
        #then lArc only needs to be a subset on host arc localLabels.
        self.direction_is_equal = direction_is_equal
        #this boolean is to distinguish that the directionality
        #within an arc matches perfectly. If false then all (singly)-directed arcs
        #will match with doubly-directed arcs, and all undirected arcs will match with all
        #directed and doubly-directed arcs. Of course, a directed arc going one way will
        #still not match with a directed arc going the other way.
        #If true, then undirected only matches with undirected, directed only with directed (again, the
        #actual direction must match too), and doubly-directed only with doubly-directed.
        self.null_means_null = null_means_null #FIXME what should the default be?
        #for a lack of a better name - this play on "no means no" applies to dangling arcs that point
        #to null instead of pointing to another node. If this is set to false, then we are saying a
        #null reference on an arc can be matched with a null in the graph or any node in the graph.
        #Like the above, a false value is like a subset in that null is a subset of any actual node.
        #And a true value means it must match exactly or in otherwords, "null means null" - null
        #matches only with a null in the host. If you want the rule to be recognized only when an actual
        #node is present simply add a dummy node with no distinguishing characteristics. That would
        #in turn nullify this boolean since this boolean only applies when a null pointer exists in
        #the rule.
        self.negate_labels = negate_labels #In GraphSynth 1.8, I added these to ruleNode, ruleArc, and embedding rule classes. This is
                                           #a simple fix and useful in many domains.
    #TODO: figure out whether or not it's import to override __deepcopy__ here
    def match_with(self, host_arc, from_host_node=None, to_host_node=None, traverse_forward=None):
        '''returns a True/False based on if the host arc matches with this rule_arc.
        host_arc = the host arc
        from_host_node = from host node
        to_host_node = to host node
        traverse_forward = since the host connecting nodes are provided, we need to
        check whether direction is an issue and that the host arc is connected forward (from
        _from to _to) or backwards.'''
        if host_arc is not None and from_host_node is not None and to_host_node is not None and traverse_forward is not None:
            if self.match_with(host_arc):
                if (self.directed and (((host_arc._to == to_host_node) and (host_arc._from == from_host_node) and traverse_forward) or ((host_arc._from == to_host_node) and (host_arc._to == from_host_node) and not traverse_forward))):
                    return True
                elif (((host_arc._to == to_host_node) and (host_arc._from == from_host_node)) or ((host_arc._from == to_host_node) and (host_arc._to == from_host_node))):
                    return True
                else: return False
            else: return False
        #what if we lack the to_node?
        if host_arc is not None and from_host_node is not None and traverse_forward is not None and to_node is None:
            if match_with(host_arc):
                if self.directed:
                    if (((host_arc._from == from_host_node) and traverse_forward is True) or ((host_arc._to == from_host_node) and not traverse_forward)): return True
                    else: return False
                elif ((host_arc._from == from_host_node) or (host_arc._to == from_host_node)): return True
                else: return False
            else: return False
        #what if we only have host_arc?
        if host_arc is not None and from_host_node is None and traverse_forward is None and to_node is None:
            #returns a true/false based on if the host arc matches with this rule_arc. This overload
            #is mostly used in the above overloads. It calls the next two functions to complete
            #the matching process.
            if host_arc is not None:
                if ((self.direction_is_equal and self.doubly_directed == host_arc.doubly_directed) and (self.directed == host_arc.directed) or (not self.direction_is_equal and (host_arc.doubly_directed or not self.directed or (self.directed and host_arc.directed and not self.doubly_directed)))):
                    #pardon my french, but this statement is a bit of a mindf**k. What it says is if
                    #directionIsEqual, then simply the boolean state of the doublyDirected and directed
                    #must be identical in L and in the host. Otherwise, one of three things must be equal.
                    #first, hostArc's doublyDirected is true so whatever LArc's qualities are, it is a subset of it.
                    #second, LArc's not directed so it is a subset with everything else.
                    #third, they both are singly directed and LArc is not doublyDirected.
                    if self.labels_match(host_arc.local_labels) and self.intended_types_match(self.arc_type, host_arc.arc_type):
                        return True
                    else: return False
            else: return False
    def labels_match(self, host_labels):
        #first an easy check to see if any negating labels exist
        #in the host_labels. if so, immediately return false.
        for label in self.negate_labels:
            if label in host_labels: return False
        #next, set up a temp_labels so that we don't change the
        #host's actual labels. We delete an instance of the label.
        #this is new in version 1.8. It's important since one may
        #have multiple identical labels.
        temp_labels = []
        temp_labels.extend(copy(host_labels))
        for label in self.local_labels:
            if label in temp_labels: temp_labels.remove(label)
            else: return False
        #this new approach actually simplifies and speeds up the containAllLabels
        #check. If there are no more tempLabels than the two match completely - else
        #return false.
        if self.contains_all_local_labels and len(temp_labels)>0: return False
        return True
    def intended_types_match(self, L_arc_type, host_arc_type):
        '''not sure what to do with this. python is dynamically typed, making all this Type stuff kinda useless.'''
        if L_arc_type is None or isinstance(L_arc_type, Arc) or isinstance(L_arc_type, RuleArc) or L_arc_type == host_arc_type:
           return True
        else: return False
    @staticmethod
    def convert_from_arc(arc):
        rule_arc = RuleArc(name=arc.name)
        rule_arc.arc_type = arc.arc_type #FIXME
        rule_arc.directed = arc.directed
        rule_arc.display_shape = arc.display_shape
        rule_arc._from = arc._from
        rule_arc.local_labels.extend(copy(arc.local_labels))
        rule_arc.local_variables.extend(copy(arc.local_variables))
        rule_arc._to = arc._to
        rule_arc.xml_arc_type = arc.xml_arc_type
        return rule_arc

class RuleNode(Node):
    '''here we define additional qualities used only by nodes in the grammar rules.'''
    graphsynth_path = "GraphSynth.Representation/RuleClasses/ruleNode.cs"
    intended_types_match = RuleArc.intended_types_match
    def __init__(self, name="", contains_all_local_labels=False, strict_degree_match=False, negate_labels=[]):
        #The following booleans capture the possible ways in which a node may/may not be a subset
        #(boolean set to false) or is equal (in this respective quality) to the host (boolean set
        #to true). These are special subset or equal booleans used by recognize. For this
        #fundamental node classes, only these two possible conditions exist.
        self.contains_all_local_labels = contains_all_local_labels
        #if true then all the localLabels in the lNode match with those in the host node, if false
        #then lNode only needs to be a subset on host node localLabels.
        self.strict_degree_match = strict_degree_match
        #this boolean is to distinguish that a particular node
        #of L has all of the arcs of the host node. Again,
        #if True then use equal
        #if False then use subset
        #NOTE: this is commonly misunderstood to be the same as induced. The difference is that this
        #applies to each node in the LHS and includes arcs that reference nodes not found on the LHS

        #In GraphSynth 1.8, I added these to ruleNode, ruleArc, grammarRule (as global Negabels) and
        #embedding rule (both for freeArc and NeighborNode) classes. This is a simple fix and useful in
        #many domains. If the host item, contains a negabel then it is not a valid match.
        self.negate_labels = negate_labels
    def match_with(self, host_node):
        '''returns True/False based on if the host node matches with this RuleNode.
        this calls the next two functions which check labels and type.'''
        if host_node is not None:
            if (((self.strict_degree_match and (self.degree == host_node.degree)) or
                (not self.strict_degree_match and (self.degree <= host_node.degree))) and
                (self.labels_match(host_node.local_labels)) and
                (self.intended_types_match(self.node_type, host_node.node_type))):
                return True
            else: return False
        else: return False
    def labels_match(self, host_labels):
        #first an easy check to see if any negating labels exist
        #in the host_labels. If so, immediately return False.
        for label in self.negate_labels:
            if label in host_labels: return False
        #next, set up a tempLabels so that we don't change the
        #host's actual labels. We delete an instance of the label.
        #this is new in version 1.8. It's important since one may
        #have multiple identical labels.
        temp_labels = []
        temp_labels.extend(copy(host_labels))
        for label in self.local_labels:
            if label in temp_labels: temp_labels.remove(label)
            else: return False
        #this new approach actually simplifies and speeds up the containAllLabels
        #check. If there are no more tempLabels than the two match completely - else
        #return False.
        if self.contains_all_local_labels and len(temp_labels)>0: return False
        return True
    @staticmethod
    def convert_from_node(n): #can't we just copy the dictionary?
        rule_node = RuleNode()
        for key in n.__dict__.keys():
            val = copy(n.__dict__[key])
            setattr(rule_node, key, val)
        return rule_node

class Option:
    '''these are presented in the choice for which rule to apply.
    option contains references to the location where the rule is
    applicable, the rule itself, along with its number in the rule_set
    and the rule_set's number when there are multiple rule_sets.'''
    graphsynth_path = "GraphSynth.Representation/RuleClasses/option.cs"
    properties = ["option_number", "rule_set_index", "rule", "location", "position_transform"]
    def __init__(self):
        #set up the properties
        for prop in self.properties:
            setattr(self, prop, property(fget=functools.partial(_get_property, attribute_name=prop), fset=functools.partial(_set_property, prop, attribute_name=prop)))
        self.option_number, self.rule_set_index, self.rule_number, self.rule, self.location, self.position_transform, self.parameters = None, None, None, None, None, None, []
    def apply(self, host, parameters=[]):
        self.rule.apply(self.location, host, self.position_transform, self.parameters)

class RuleSet: #not done yet
    '''As far as I can tell, this is the first time the idea of a rule set
    has been developed to this degree. In many applications we find that
    different sets of rules are needed. Many of these characteristics
    are built into our current generation process.'''
    graphsynth_path = "GraphSynth.Representation/RuleClasses/ruleSet.Basic.cs"
    choice_method = property(fget=functools.partial(_get_property, attribute_name="choice_method"), fset=functools.partial(_set_property, attribute_name="choice_method")) #why does this have to be a property?
    

    def __init__(self, name="", rules=[], rule_file_names=[], trigger_rule_number=-1, next_generation_steps=NextGenerationSteps(), rule_set_index=None):
        '''
        Please note that rule numbers are *not* zero-based. The first rule is number 1.

        name: #an arbitrary name for the RuleSet - usually set to the filename
        trigger_rule_number: A ruleSet can have one rule set to the triggerRule. If there is no
                            triggerRule, then this should stay at negative one (or any negative
                            number). When the trigger rule is applied, the generation process, will
                            exit to the specified generationStep (as described below).
        next_generation_steps: For a particular set of rules, we need to specify what generation should
                               do if any of five conditions occur during the recognize->choose->apply
                               cycle. The enumerator, nextGenerationSteps, listed in globalSettings.cs
                               indicates what to do. The five correspond directly to the five elements
                               of another enumerator called GenerationStatuses. These five possibilties are:
                               Normal, Choice, CycleLimit, NoRules, TriggerRule. So, following normal operation
                               of RCA (normal), we perform the first operation stated below, nextGenerationStep[0]
                               this will likely be to LOOP and contine apply rules. Defaults for these are
                               specified in App.config.
        rule_set_index: For multiple ruleSets, a value to store its place within the set of ruleSets
                        proves a useful indicator.
        '''
        #cheap way of not having to type a lot to make up properties with the same generational structure, syntax and function
        _compress_props = [("generation_after_normal", 0), ("generation_after_choice", 1), ("generation_after_cycle_limit", 2), ("generation_after_no_rules", 3), ("generation_after_trigger_rule", 4)]
        for each in _compress_props:
            setattr(self, each[0], property(fget=functools.partial(_get_property, attribute_name=each[0], attr_index=each[1]), fset=functools.partial(_set_property, attribute_name=each[0], attr_index=each[1])))
        self.name = name 
        self.choice_method = ChoiceMethods.design
        #Often when multiple ruleSets are used, some will produce feasible candidates,
        #while others will only produce steps towards a feasible candidate. Here, we
        #classify a particular ruleSet as one of these.
        self.interim_candidates = CandidatesAre.unspecified
        self.final_candidates = CandidatesAre.unspecified
        #the rules are clearly part of the set, but these are not stored
        #in the XML, only the ruleFileNames. In ruleSetXMLIO.cs the
        #loading of rules is accomplished.
        self.rules = rules
        self.rule_file_names = rule_file_names
        self._trigger_rule_number = trigger_rule_number
        self.next_generation_steps = next_generation_steps
        self.rule_set_index = rule_set_index
        self.filer = None
    def next_rule_set(self, status):
        '''A helper function to RecognizeChooseApplyCycle. This function returns what the new ruleSet
        will be. Here the enumerator nextGenerationSteps and GenerationStatuses is used to great
        affect. Understand that if a negative number is returned, the cycle will be stopped.'''
        if self.next_generation_step[status] == NextGenerationSteps.loop: return self.rule_set_index
        elif self.next_generation_step[status] == NextGenerationSteps.go_to_next: return self.rule_set_index + 1
        elif self.next_generation_step[status] == NextGenerationSteps.go_to_previous: return self.rule_set_index - 1
        else: return int(self.next_generation_step[status])
    def recognize(self, host):
        '''This is the recognize function called within the RCA generation. It is
        fairly straightforward method that basically invokes the more complex
        recognize function for each rule within it, and returns a list of options.'''
        options = []
        if len(self.rules) == 0: return options
        option_num = 0
        i = 0
        for rule in self.rules:
            i = self.rules.index(rule)
            transform_matrices = []
            locations = [] #a list of Graphs
            locations = self.rules[i].recognize(host, transform_matrices)
            j = 0
            for loc in locations:
                j = locations.index(loc)
                option = Option()
                options.append(option)
                temp=option_num+1
                option.option_number = temp #FIXME or should option_num be set to option_num+1? see GS codebase
                option.rule_set_index = self.rule_set_index
                option.rule_number = i + 1
                option.rule = rule
                option.location = loc
                option.position_transform = transform_matrices[j]
                if self.choice_method == choiceMethods.Automatic: return options
                #this is merely for efficiency - once we get one valid option for
                #an Automatic ruleset we can exit and invoke that option.
            return options

class EmbeddingRule:
    '''the freeArc can be identified by one of the following
    1. label of dangling arc in D (freeArcLabel)
    2. name of node in L-R that arc was recently attached to (note the name is from L not G) (L_node_name)
    3. label of node in G that is currently attached to dangling arc in D (neighborNodeLabel)
    -----
    the RHS of the rule is simply the name of the R-node that the arc is to connect to. Since
    this exists within the rule, there is no need to include any other defining character - of
    course we still need to find the corresponding node in H1 to connect it to. Note, this is
    also the main quality that distinguishes the approach as NCE or NLC, as the control is given
    to the each individual of R-L (or the daughter graph in the NCE lingo) as opposed to simply
    a label based method.'''
    def __init__(self, free_arc_labels=[], free_arc_negabels=[], neighbor_node_labels=[], neighbor_node_negabels=[], L_node_name=None, original_direction=None, new_direction=None, allow_arc_duplication=False):
        '''
        allow_arc_duplication: if True, then for each rule that matches with the arc the arc will be duplicated.
        '''
        self.free_arc_labels = free_arc_labels
        self.free_arc_negabels = free_arc_negabels
        self.neighbor_node_labels = neighbor_node_labels
        self.neighbor_node_negabels = neighbor_node_negabels
        self.L_node_name = L_node_name
        self.original_direction = original_direction
        self.new_direction = new_direction
        #in order to give the edNCE approach the "ed" quality, we must allow for the possibility of
        #recognizing arcs having a particular direction. The original direction can be either +1 meaning
        #"to", or -1 meaning "from", or 0 meaning no imposed direction - this indicates what side of the
        #arc is dangling. Furthermore, the newDirection, can specify a new direction of the arc ("to",
        #or "from" being the new connection) or "" (unspecified) for updating the arc. This allows us
        #to change the direction of the arc, or keep it as is.
        self.allow_arc_duplication = allow_arc_duplication
    def arc_is_free(self, arc, host):
        if arc._from is not None and arc._to is not None and (arc._from not in host.nodes) and (arc._to not in host.nodes):
            self.free_end_identifier=0
            #if the nodes on either end of the freeArc are pointing to previous nodes
            #that were deleted in the first pushout then neighborNode is null (and as
            #a result any rules using the neighborNodeLabel will not apply) and the
            #freeEndIdentifier is zero.
            self.neighbor_node = None
            return True
        elif arc._from is not None and arc._from not in host.nodes:
            self.free_end_identifier = -1
            #freeEndIdentifier set to -1 means that the From end of the arc must be the free end.
            self.neighbor_node = arc._to
            return True
        elif arc._to is not None and arc._to not in host.nodes:
            self.free_end_identifier = +1
            #freeEndIdentifier set to +1 means that the To end of the arc must be the free end.
            self.neighbor_node = arc._from
            return True
        else:
            #else, the arc is not a free arc after all and we simply break out
            #of this loop and try the next arc.
            self.free_end_identifier = 0
            self.neighbor_node = None
            return False
    def find_new_node_to_connect(self, R, R_mapping):
        #find R-L node that is to be connected with freeArc as well as old L-R node name
        if self.R_node_name is not None and self.R_node_name is not "":
            #take the RNodeName from within the rule and get the proper reference to the new node.
            #If there is no RNodeName, then the embedding rule will set the reference to null.
            index = R.find_index_of_node_with(name=self.R_node_name)
            return R_mapping.nodes[index]
        else: return None
    def find_deleted_node(self, L, L_mapping):
        #similarly, we can find the LNodeName (if one exists in this particular rule). Setting this
        #up now saves time and space in the below recognition if-then's.
        if self.L_node_name is not None and self.L_node_name is not "":
            index = L.find_index_of_node_with(name=self.L_node_name)
            return L_mapping.nodes[index]
        else: return None
    def rule_is_recognized(free_end_identifier, free_arc, neighbor_node, node_removed):
        #this one is a little bit of enigmatic but clever coding if I do say so myself. Both
        #of these variables can be either +1, 0, -1. If in multiplying the two together you
        #get -1 then this is the only incompability. Combinations of +1&+1, or +1&0, or
        #-1&-1 all mean that the arc has a free end on the requested side (From or To).
        raise NotImplementedError, bryan_message

#########
#land of no implementations
#########

class SearchProcess:
    def __init__(self):
        pass
    def run(self):
        '''implements a random search'''
        pass
    def is_current_the_goal(self, m):
        if m.f2 == 0.0: return True
        return False
    def transfer_L_mapping_to_child(self, child, current, L_mapping):
        '''this is a subtle issue with recognize-choose-apply in a Tree Search.
        The locations within each option are pointing to nodes and arcs within the current.graph,
        but we would like to retain the current so we make a deep copy of it. This is fine but now
        the locations need to be transfered to the child. That is why this function was created.'''
        raise NotImplementedError, bryan_message_generator("GraphSynthSourceFiles/GraphSynth.Search/searchProcess.cs")
        #delegate
        for arc in L_mapping.arcs:
            i = L_mapping.arcs.index(arc)
            the_arc = find_delegate(current.arcs, arc)[0] #[0] because we want the first
            position = current.arcs.index(the_arc)
            L_mapping.arcs[i] = child.arcs[position]
        for node in L_mapping.nodes:
            i = L_mapping.nodes.index(node)
            the_node = find_delegate(current.nodes, node)
            position = current.nodes.index(the_node)[0]
            L_mapping.nodes[i] = child.nodes[position]
    def next_rule_set(self, rule_set_index, status):
        '''A helper function to RecognizeChooseApplyCycle. This function returns what the new ruleSet
        will be. Here the enumerator nextGenerationSteps and GenerationStatuses is used to great
        affect. Understand that if a negative number is returned, the cycle will be stopped.'''
        if self.rulesets[rule_set_index].nextGenerationStep[int(status)] == nextGenerationSteps.Loop:
            return rule_set_index
        elif self.rulesets[rule_set_index].nextGenerationStep[int(status)] == nextGenerationSteps.GoToNext:
            return rule_set_index+1
        elif self.rulesets[rule_set_index].nextGenerationStep[int(status)] == nextGenerationSteps.GoToPrevious:
            return rule_set_index-1
        else:
            return int(self.rulesets[rule_set_index].nextGenerationStep[int(status)])
    @staticmethod
    def calculate_f0(f1, f2, average_time):
        return ((20.0 * f1 / average_time) + f2)
    def add_new_cand_to_pareto(self, candidate, pareto_cands):
        for pc in pareto_cands:
            if self.dominates(candidate, pc):
                pareto_cands.remove(pc)
                print "g: ", c.f1, ", h: ", c.f2
            elif self.dominates(pc, c): return
        pareto_cands.append(candidate)
        return pareto_cands
    @staticmethod
    def add_child_to_sorted_cand_list(candidates, child):
        if len(canddiates)==0: candidates.append(child)
        else:
            i = 0
            f_child = child.f0
            while i<len(candidates) and f_child>= candidates[i].f0:
                i=i+1
            canddiates.insert(i, child)
    @staticmethod
    def kill_off_clones(new_children):
        last_rule_position = len(new_children[0].recipe)-1
        raise NotImplementedError, bryan_message #line 104 in searchProcess.cs

