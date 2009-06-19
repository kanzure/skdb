#!/usr/bin/python
# Bryan Bishop (kanzure@gmail.com) http://heybryan.org/
# 2009-06-14
# find-all-cutsets.py - find all of the cutsets in a graph
import graph as pygraph # for pygraph 1.5
import copy
import unittest
#import sets from Set

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield frozenset(tuple(pool[i] for i in indices))
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield frozenset(tuple(pool[i] for i in indices))

#for counter in range(len(graph.edges()):
#        combinations(graph.edges(),counter)


def find_all_paths(graph, start, end, path=[]):
        #http://www.python.org/doc/essays/graphs/
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


# a graph is connected if there is a path to go from any given two vertices (ignoring directions)
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

def makeCut(cutset,g):
        # make a cut in graph g by removing the edges in the cutset list.
        returng = copy.copy(g)
        multipleCuts = False
        print "the len of the cutset is: ", len(cutset)
        if len(cutset) > 2:
                multipleCuts = True
        if multipleCuts:
                for each in cutset:
                        #print "about to delete the following edge: ", each[0], each[1]
                        #print "the list of each is:\t", list(each)
                        if (returng.has_edge(list(each)[0],list(each)[1])):
                                returng.del_edge(list(each)[0],list(each)[1])
        elif not multipleCuts and len(cutset)>1:
                if returng.has_edge(list(cutset)[0],list(cutset)[1]):
                        returng.del_edge(list(cutset)[0],list(cutset)[1])
        return returng # return this new graph.

#def removeDupes(cutsetlist):
#        # set([frozenset((1,2)),frozenset((3,4))]) == set([frozenset((2,1)),frozenset((3,4))])
#        # True
#        listOfSets = []
#        for each in cutsetlist:
#              thisSet = set()
#              for edge in each:
#                thisSet.add(frozenset(edge))
#              listOfSets.append(thisSet)
#        for each in listOfSets:
#                for other in listOfSets:
                

#g = pygraph.graph()
#g.add_nodes(range(1,20))
#assertTrue(isGraphConnected(g))

# f-cutset algorithm
# an f-cutset is made up of a single branch and a unique set of chords
# 
# remove the root (given) branch. if the graph is not divided, repeat. if it is, add that branch to the return set.

# this probably has to be rewritten
def cutset(fromNode, toNode, graph, level=0):
   if not (graph.has_edge(fromNode, toNode)):
      return []
   print "cutset level level =",level,"\n"
   graph2 = copy.copy(graph)
   rset = [(fromNode, toNode)] # return set (we assume it starts with this edge at least)
   print "function cutset: graph is ", graph2
   print "removing:\n\tfromNode = ", fromNode, "\n\ttoNode = ", toNode, "\n"
   graph2.del_edge(fromNode, toNode)
   print "function cutset (2): graph is ", graph2
   if isGraphConnected(graph2): # graphDivided()
      print "the graph is connected!\n"
      for each in graph2.edges():
         #if (each[0] and each[1]):
         print "level=",level," .. each var is: ", each
         extension = cutset(each[0],each[1],copy.copy(graph2),level+1)
         if extension:
            rset.extend(extension) #cutset(each[0],each[1],copy.copy(graph2),level+1))
   print "leaving cutset level level=",level,"\n"
   return rset

# now for some testing.

class TestCut(unittest.TestCase):
   def test_isGraphConnected(self):
      g = pygraph.graph()
      g.add_nodes(range(1,20))
      self.assertFalse(isGraphConnected(g))
      for each in range(1,19):
         g.add_edge(each,each+1)
      print "graph is ", g
      self.assertTrue(isGraphConnected(g))
            
      # 1-2-3 cutsets: [[(1,2)], [(2,3)]
      g = pygraph.graph() # still not using a digraph
      g.add_nodes([1,2,3,4,5,6,7,8,9])
      g.add_edge(1,2)
      g.add_edge(2,3)
      g.add_edge(3,4)
      g.add_edge(4,5)
      g.add_edge(5,6)
      g.add_edge(6,7)
      g.add_edge(7,8)
      g.add_edge(8,9) # so, 8 individual different cutsets, right?
      print "graph is ", g
      thecutset = cutset(7,8,g)#(1,2,g)
      print "thecutset = ", thecutset
      self.assertTrue(len(thecutset)==1)

      # more complicated graph


      # testing combinations()
      print "testing combinations().\n\n"

      com = combinations((1,2,3,4,5),3)
      print frozenset(com)
      for each in com:
        print "tiny is", each
      raw_input("done testing combinations?")

      # find all possible cutsets.
      print "\n\nfind all possible cutsets.\n"
      cutsetlist = set()
      for counter in range(len(g.edges())):
         stuff = combinations(g.edges(),counter)
         print "here are the combinations of g.edges() for counter = ", counter
         print frozenset(stuff)
         raw_input("continue?")
         for tinystuff in stuff:
                cutsetlist.add(frozenset(tinystuff))
      
      print ".. done making the cutsetlist.\n"
      #print "cutsetlist is: ", cutsetlist
      #print "\n\n\n"
      
      realCutSets = set()

      # now shorten the list of cutsets.
      for each in cutsetlist:
        #print "the length of this cutset was .. ", len(each)
        #print "\t", each
        theCutGraph = makeCut(each,g)
        if not isGraphConnected(theCutGraph):
                # "each" is indeed a cutset.
                realCutSets.add(each)#frozenset(each))
      
      # clean up the list.

      # remove duplicates. for instance, if the list has (4,6) and (6,4), remove one of them.
      #realCutSets = removeDupes(realCutSets)
    
      # now inform the user which ones were really cutsets.
      for each in realCutSets:
        print "a real cutset was: ", each
        #raw_input("continue?")

      print "END.\n\n\n"
      # TODO: try pygraph.digraph(). for checking connectedness it should ignore direction.
      # for path finding, directionality does matter in a digraph.

if __name__ == '__main__':
   unittest.main()


