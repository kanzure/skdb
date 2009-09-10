#!/usr/bin/python
import math
import yaml #maybe one day?
from copy import copy

def set_list(self, variable, index, label):
    '''called a few times in Arc, like in set_label and set_variable'''
    while len(variable) <= index:
        variable.append("")
    variable[index] = label

class Arc:
    
    #these dont need to be here (just for reference)
    name = ""
    _to = None #head
    _from = None #tail
    directed = False
    doubly_directed = False
    local_labels = []
    local_variables = []
    old_data = {'style_key': "", 'x': "", 'y': ""}

    def __init__(self, name="", from_node=None, to_node=None):
        self.name = name
        self._from = from_node
        self._to = to_node
    def set_to(self, to):
        self._to = to
    def set_from(self, from1):
        self._from = from1
    def from(self):
        return self._from
    def to(self):
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

    def __init__(self, name=""):
        self.name = name
    def degree(self):
        '''the degree or valence of a node is the number of arcs attached to it.
        currently this is used in recognition of rule when the strictDegreeMatch is True.'''
        return len(self.arcs)
    self.set_label = Arc.set_label
    self.set_variable = Arc.set_variable

class Vertex(Node):
    #this was blank in the graphsynth codebase for some reason?
    pass

class DesignGraph:
    
    #just for reference
    name = ""
    global_labels = []
    global_variables = []
    arcs = []
    nodes = []

    def __init__(self, count=None, nodes=None, arcs=None):
        '''set count to some number to make this a complete graph of that many nodes.
        note: average_degree is currently not implemented (to make a graph with an average degree on each node)
        '''
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
        raise NotImplementedError, "bryan hasnt got this far yet"
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
            raise ValueError, "DesignGraph.add_arc must be given at least one parameter."
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
            raise IndexError, "DesignGraph.remove_arc: identifier not in list."
        return
    def add_node(self, new_name="", node_ref=None):
        if node_ref is not None and new_name is not None:
            raise ValueError, "DesignGraph.add_node: can't both add the node and make a node with the new name, do it yourself."
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
        if node_index is None and node_ref is None: raise ValueError, "DesignGraph.remove_node: must be given either a node or a node_index"
        if node_index is not None:
            if node_index > len(self.nodes)-1: raise IndexError, "DesignGraph.remove_node: node_index is bad."
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

    #just for reference:
    previous_states = [] #a list of DesignGraph objects
    current_state = None #a DesignGraph
    _graph = None
    recipe = []
    performance_params = []
    active_rule_set_index = -1
    age = -1 #the number of iterations this graph has gone through (set by the search process)
    generation_status = []

    def __init__(self, graph=None):
        self._graph = graph
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

##### no-man's land
#this is only from grammarRule.Basic.cs
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
    locations = [] #list of DesignGraph objects
    L = None #DesignGraph
    R = None #DesignGraph

    def no_other_arcs_in_host(self, host_graph, located_nodes, located_arcs):
        pass
    def labels_match(self, host_labels=[]):
        if self.ordered_global_labels: return self.order_labels_match(host_labels)
        else: return self.unordered_labels_match(host_labels)
    def order_labels_match(self, host_labels=[]):
        pass
    def unordered_labels_match(self, host_labels=[]):
        pass
    def make_unique_node_name(self):
        pass
    def make_unique_arc_name(self):
       pass

