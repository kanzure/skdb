#!/usr/bin/python
import math
import yaml #maybe one day?
from numpy import identity, multiply
from copy import copy
import functools
import unittest

campbell_message = "campbell didnt implement this"
bryan_message = "bryan hasnt got that far yet"
def bryan_message_generator(path): return bryan_message + (" (%s)" % (path))

#in the original graphsynth codebase, there were a lot of properties
#these need to be reincorporated into this version
def _set_property(self, value=None, attribute_name=None):
    assert attribute_name, "_set_property must have an attribute name to work with"
    setattr(self, attribute_name, value)
def _get_property(self, attribute_name=None):
    assert attribute_name, "_get_attribute must have an attribute name to work with"
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

def set_list(self, variable, index, label):
    '''called a few times in Arc, like in set_label and set_variable'''
    while len(variable) <= index:
        variable.append("")
    variable[index] = label

def make_identity(size):
    return identity(size)

class Arc:
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

class Edge(Arc):
    '''Originally, I created a separate edge and vertex class to allow for the future expansion of GraphSynth into shape grammars. I now have decided that the division is not useful, since it simply deprived nodes of X,Y,Z positions. Many consider edge and arc, and vertex and node to be synonymous anyway but I prefer to think of edges and vertices as arcs and nodes with spatial information. At any rate there is no need to have these inherited classes, but I keep them for backwards-compatible purposes.'''
    #there isn't actually any code for an Edge
    pass    

class Node:
    #none of this has to be here, it's just for reference
    name = ""
    local_labels = []
    local_variables = []
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
    set_label = Arc.set_label
    set_variable = Arc.set_variable

class Vertex(Node):
    #this was blank in the graphsynth codebase for some reason?
    pass

class Graph:
    def __init__(self, count=None, nodes=None, arcs=None, global_labels=[], global_variables=[]):
        '''set count to some number to make this a complete graph of that many nodes.
        note: average_degree is currently not implemented (to make a graph with an average degree on each node)
        '''
        self.global_labels = global_labels
        self.global_variables = global_variables
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
        latest = None
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

class Candidate:
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
        assert NotImplementedError, "bryan hasnt got around to this yet"
    def save_to_yaml(self, filename=None):
        '''not guaranteed to be pretty'''
        assert NotImplementedError, "Candidate.save_to_yaml: bryan hasnt got around to implementing yaml dumps yet"
        handler = open(filename, 'w')
        handler.write(yaml.dump(self, default_flow_style=False))
        handler.close()

class Rule: #GrammarRule
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
        pass
    #more ...
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

