#!/usr/bin/python
import graph as pygraph
import copy
import unittest
#from sets import Set

def combinations(iterable, r):
    # http://docs.python.org/library/itertools.html#itertools.combinations
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def find_all_paths(graph, start, end, path=[]):
        # http://www.python.org/doc/essays/graphs/
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_node(start):
            return []
        paths = []
        #print "current path is: ", path
        for node in graph.neighbors(start):
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

def find_cycle(graph):
    cycles=[]
    for startnode in graph.nodes():
        for endnode in graph.nodes():
            newpaths = find_all_paths(graph, startnode, endnode)
            for path in newpaths:
               if len(path)>2:
                  if path[0] in graph.neighbors(path[len(path)-1]):
                     path.append(path[0])
                     cycles.append(path)
                #if(len(path)>2):
                #  path.append(path[0])
                #  cycles.append(path)
                #if (len(path)==len(graph)):
                #    if path[0] in graph.neighbors(path[len(graph)-1]):
                #        #print path[0], graph[path[len(graph)-1]]
                #        path.append(path[0])
                #        cycles.append(path)
    return cycles

# Set(A).intersection(B) == len(A) and len(A) == len(B)
# [[16, 17, 18, 13, 14, 15, 16], [18, 13, 14, 15, 16, 17, 18]]
#def reduceCycles(cycles):
#   for cycle in cycles:
#      for ocycle in cycles:
#         match = False
#         if (len(cycle) == len(ocycle)) and not (cycle == ocycle): # if they have the same path lengths
#            print "set intersection is: ", Set(cycle).intersection(ocycle), " and length is: ", len(Set(cycle).intersection(ocycle))
#            if (len(Set(cycle).intersection(ocycle)) == len(cycle)-1): # note that the cycle has an extra node in it (the last node in the path)
#               # they are the same cycle. blasphemy!
#               match = True
#         if match:
#            print "match between:\n\t", cycle, "\n\t", ocycle, "\n\n"
#            cycles.remove(ocycle)
#   return cycles 

#def doReduction(cycles):
#   oldcycles = copy.copy(cycles)
#   if(len(cycles) > 0):
#      while(len(cycles) == len(oldcycles)):
#         cycles = reduceCycles(cycles)
#   return cycles

def isGraphConnected(graph): # deprecated
   # FIXME: countGraphs(g) is probably more efficient than using isGraphConnected()
   pathExists = True
   #print "isGraphConnected: number of edges = ", len(graph.edges())
   if len(graph.edges()) == 0: # graph can't be connected with no edges
      return False
   for node in graph.nodes():
      for onode in graph.nodes():
         paths = find_all_paths(graph, node, onode)
         if (paths == []):
            pathExists = False
   return pathExists

def countGraphs(g): 
        # count the number of graphs in g.
        if (len(g.nodes()) == 0):
                return 0
        elif (len(g.nodes()) == 1):
                return 1
        dict = pygraph.accessibility.connected_components(g)
        return len(list(frozenset(dict.values())))

def makeCut(cutset,g):
        # make a cut in graph g by removing the edges in the cutset list.
        # if no cut is made, returns the original graph
        returng = copy.deepcopy(g)
        multipleCuts = False
        # print "the len of the cutset is: ", len(cutset)
        if len(cutset) >= 2:
                #print "the type is: ", type(cutset[0]), " and type int is: ", type(int())
                if not (type(cutset[0]) == type(int())): # FIXME not all nodes are int() objects; maybe check that it's not a list? (er, type(list))
                        if len(cutset[0]) > 0:
                                multipleCuts = True
        if multipleCuts:
                for each in cutset:
                        #print "about to delete the following edge: ", each[0], each[1]
                        #print "the list of each is:\t", list(each)
                        if (returng.has_edge(list(each)[0],list(each)[1])): # used to be: list(each)[0], list(each)[1] ; used to be: each[0], each[1]
                                returng.del_edge(list(each)[0],list(each)[1]) # used to be: list(each)[0], list(each)[1]
        elif not multipleCuts and len(cutset)>1:
                if returng.has_edge(cutset[0],cutset[1]):
                        returng.del_edge(cutset[0],cutset[1])
        return returng # return this new graph.

# g = pygraph.graph or pygraph.digraph object
# howManyResultingGraphs = include a cutset only if it makes this many graphs out of the original given graph.
# howManySets = the number of sets to create (=0 implies "go wild")
def cutsets(g, howManyResultingGraphs = 2, howManySets = 0):
        # find all cutsets in graph g. return them.
        returnlist = [] # no cutsets yet
        createdSets = 0
        for each in range(1,len(g.edges())):
                if ((howManySets!=0 and createdSets<howManySets) or (howManySets == 0)):
                        com = list(combinations(g.edges(),each)) # list() unrolls the generator object (from combinations())
                        for each in com: # for each cut within the cutset,
                                if ((howManySets!=0 and createdSets<howManySets) or (howManySets == 0)):
                                        # try this cut.
                                        # some modifications ..
                                        if len(each)==1: each = list(each[0]) # thanks bingogas_station
                                        g2 = makeCut(each,g)
                                        if 1==1: #if not isGraphConnected(g2):
                                                counter = countGraphs(g2)
                                                #if counter==1: print "g2 = ", g2, "\n\tcounter = ", counter, "\t", each, "\t len(each)= ", len(each)
                                                if counter == howManyResultingGraphs:
                                                        #print "cut found: ", each
                                                        returnlist.append(each)
                                                        createdSets=createdSets+1
        #print "cutsets() exiting after creating \t", createdSets, "\t cutsets.\n"
        return returnlist

def separateGraphs(g):
        # given a graph g with non-connected components, return each component separately.
        # there's countGraphs(g) number of graphs to find in g.
        graphs = []
        #dict = pygraph.accessibility.connected_components(g)
        #len(list(frozenset(dict.values())))
        thedict = pygraph.accessibility.connected_components(g)
        # there's len(frozenset(thedict.keys())) number of graphs to be returned.
        for each in list(frozenset(thedict.values())):
                if type(g) == type(pygraph.graph):
                        g2 = pygraph.graph()
                if type(g) == type(pygraph.digraph):
                        g2 = pygraph.digraph()
                else:
                        print "ERROR: unknown graph type.\n"
                        return
                for node in thedict.keys():
                        if thedict[node] == each:
                                g2.add_node(node)
                                # also, add the edges corresponding to this node in this component
                                for edge in g.edges():
                                        if edge[0] == node or edge[1] == node:
                                                g2.add_edge(edge[0],edge[1])
                graphs.append(g2)
        return graphs

def extractAcrossVariables(node):
        acrossvariables = []
        return acrossvariables

def extractThroughVariables(node):
        throughvariables = []
        return throughvariables

def equationsFromCutsets(g,cutsets): # KCL (Kirchhoff's Circuit Law)
        # McPhee's Vertex Postulate: the sum of through variables at any node of a system graph must equal zero when due account is taken of the orientation of edges incident upon that node.
        # Each fundamental cutset breaks the circuit into two pieces: two supernodes. Write a KCL equation for one supernode in each f-cutset (in terms of node voltages). The KCL equations for the two supernodes formed by an f-cutset will be the same. This yields n-1 equations in n node voltage variables. Set one node voltage to zero volts (ground) and solve.
        equations = []
        for cutset in cutsets:
                # TODO: check whether or not the cutset is an f-cutset for the graph
                g2 = makeCut(cutset,g)
                graphs = separateGraphs(g2)
        return equations

def equationsFromCycles(g,cycles): # KVL (Kirchhoff's Voltage Law)
        # McPhee's Circuit Postulate: the sum of across variables around any circuit of a graph must equal zero when due account is taken of the direction of edges in the circuit.
        # each variable in the overall graph is given a unique global name.
        equations = []
        for cycle in cycles:
                allAcrossVariables = []
                # for each node in a cycle
                for node in cycle:
                        # extract the across variables at a node
                        acrossvars = extractAcrossVariables(node)
                        # add these to the list for this cycle
                        allAcrossVariables.expand(acrossvars)
                sumEquation = "" # start off with nothing.
                for each in allAcrossVariables:
                        sumEquation = sumEquation + each + "+ "
                sumEquation = sumEquation + " 0 = 0"
                equations.append(sumEquation)
        return equations

def equationsFromNodes(g):
        equations = []
        return equations

# unit tests

class TestMisc(unittest.TestCase):
        def test_separateGraphs(self):
                # there should be countGraphs(g) number of graphs returned by separateGraphs(g)
                g = pygraph.graph()
                g.add_nodes(range(1,11)
                for each in range(1,10):
                        g.add_edge(each,each+1)
                gcut1 = makeCut([1,2],g)
                counter = countGraphs(gcut1)
                graphs = separateGraphs(g)
                self.assertTrue(counter==len(graphs))

class TestCycle(unittest.TestCase):
        #def test_find_all_paths(self):
        #        # not sure we care about this enough
        #        #print "test_find_all_paths"
        #        return
        def test_find_cycle(self):
                g = pygraph.graph()
                g.add_nodes(range(1,11))
                for each in range(1,10):
                        g.add_edge(each,each+1)
                g.add_edge(1,10)
                g2 = copy.deepcopy(g)
                # also, try one with another edge thrown in there
                g2.add_edge(2,5) 
                cycles = find_cycle(g)
                cycles2 = find_cycle(g2)
                #print "g = ", g
                #print cycles
                reducedCycles = set()
                for each in cycles:
                        reducedCycles.add(frozenset(each))
                trulyReducedCycles = frozenset(reducedCycles)
                # there should only be one cycle
                self.assertTrue(len(trulyReducedCycles)==1)
                
                reducedCycles2 = set()
                for each in cycles2:
                        reducedCycles2.add(frozenset(each))
                trulyReducedCycles2 = frozenset(reducedCycles2)
                self.assertTrue(len(trulyReducedCycles2)==3)

                # TODO: pygraph.digraph

        # the following were superceded by the use of frozenset
        #def test_reduceCycles(self):
        #        print "test_reduceCycles"
        #def test_doReduction(self):
        #        print "test_doReduction"

class TestCutSet(unittest.TestCase):
        def test_isGraphConnected(self):
                # make a graph
                g = pygraph.graph()
                # add some nodes
                g.add_nodes(range(1,20))
                self.assertFalse(isGraphConnected(g))

                # add some edges, make the graph connected.
                for each in range(1,19):
                        g.add_edge(each,each+1)
                self.assertTrue(isGraphConnected(g))

                g.del_edge(1,2)
                self.assertFalse(isGraphConnected(g))

                # TODO: digraph tests

        def test_combinations(self):
                # combinations() actually exists in python 2.6 as itertools.combinations()
                
                # very simple test.
                simpleTest = [1,2,3,4,5]
                simplecom = combinations(simpleTest,1)
                simplecom = list(simplecom)
                self.assertTrue(len(simplecom) == len(simpleTest))
                #stillsimplecom = list(combinations(simpleTest,2)) 

                # make a directed graph
                g = pygraph.digraph()
                # add some nodes
                g.add_nodes(range(1,11))
                # add some edges
                for each in range(1,10):
                        g.add_edge(each,each+1)
                # get the combinations
                com = combinations(g.edges(),3)
                # don't want a generator
                com = list(com)
                # don't want dupes.
                com2 = frozenset(copy.copy(com))
                self.assertTrue(com!=com2)

        def test_makeCut(self):
                # blah?

                # start with a non-directed graph.
                g = pygraph.graph()
                # add some nodes
                g.add_nodes(range(1,11))
                # add some edges
                for each in range(1,10):
                        g.add_edge(each,each+1)
                # make a single cut
                gcut1 = makeCut([1,2],g)
                # should be two less edges because both (1,2) and (2,1) should have been removed.
                self.assertTrue(len(gcut1.edges()) == len(g.edges())-2)
                gcut2 = makeCut(([1,2],[3,4]),g)
                self.assertTrue(len(gcut2.edges()) == len(g.edges())-4)
                gcut3 = makeCut(([1,2],[3,4],[4,5]),g)
                self.assertTrue(len(gcut3.edges()) == len(g.edges())-6)

                # directed graph test
                g2 = pygraph.digraph()
                # add some nodes
                g2.add_nodes(range(1,11))
                # add some edges
                for each in range(1,10):
                        g2.add_edge(each,each+1)
                # make a single cut
                g2cut1 = makeCut([1,2],g2)
                self.assertTrue(len(g2cut1.edges()) == len(g2.edges())-1)
                # make two cuts
                g2cut2 = makeCut(([1,2],[2,3]),g2)
                self.assertTrue(len(g2cut2.edges()) == len(g2.edges())-2)

        def test_countGraphs(self):
                g = pygraph.graph()
                g.add_nodes(range(1,11))
                for each in range(1,10):
                        g.add_edge(each,each+1)
                self.assertTrue(countGraphs(g)==1)
                g1cut1 = makeCut([1,2],g)
                self.assertTrue(countGraphs(g1cut1)==2)
                g1cut2 = makeCut(([1,2],[3,4]),g)
                self.assertTrue(countGraphs(g1cut2)==3)

        def test_countGraphs_digraph(self):
                g = pygraph.digraph()
                g.add_nodes(range(1,11))
                for each in range(1,10):
                        g.add_edge(each,each+1)
                self.assertTrue(countGraphs(g)==1)
                g1cut1 = makeCut([1,2],g)
                self.assertTrue(countGraphs(g1cut1)==2)

        def test_cutsets(self):
                # this is the big one.
                # total number of f-cutsets in a given graph = (len(g.nodes())-1)

                # start with a non-directed graph
                g = pygraph.graph()
                # add some nodes.
                g.add_nodes(range(1,11))
                # add some edges
                for each in range(1,10):
                        g.add_edge(each,each+1)

                # find all cutsets that divide the graph into 2 graphs.
                # the third parameter is set to the max number of cuts to return
                # in this case, we know that there are at most 9 cuts,
                # (because of the 9 edges)
                gsets = cutsets(g,2,len(g.edges())/2)
                self.assertTrue(len(gsets)==len(g.edges())/2) # this only holds for pygraph.graph (not pygraph.digraph)
                self.assertTrue(len(gsets)==len(g.nodes())-1)

                # directed graph test.
                g2 = pygraph.digraph()
                g2.add_nodes(range(1,11))
                for each in range(1,10):
                        g2.add_edge(each,each+1)
                self.assertTrue(countGraphs(makeCut([1,2],g2)) == 2)
                g2sets = cutsets(g2,2)
                self.assertTrue(len(g2sets)==len(g.nodes())-1)

if __name__ == '__main__':
        unittest.main()
