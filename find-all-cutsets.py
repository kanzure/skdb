#!/usr/bin/python
import graph as pygraph
import copy
import unittest

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

def isGraphConnected(graph):
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

# unit tests
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
                # total number of cutsets in a given graph = (len(g.nodes())-1)

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
