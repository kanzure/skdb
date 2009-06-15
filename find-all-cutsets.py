#!/usr/bin/python
# Bryan Bishop (kanzure@gmail.com) http://heybryan.org/
# 2009-06-14
# find-all-cutsets.py - find all of the cutsets in a graph
import pygraph
import copy
import unittest

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
   for node in graph.nodes():
      for onode in graph.nodes():
         paths = find_all_paths(graph, node, onode)
         if (paths == []):
            pathExists = False
   return pathExists

#g = pygraph.graph()
#g.add_nodes(range(1,20))
#assertTrue(isGraphConnected(g))

# f-cutset algorithm
# an f-cutset is made up of a single branch and a unique set of chords
# 
# remove the root (given) branch. if the graph is not divided, repeat. if it is, add that branch to the return set.

def cutset(fromNode, toNode, graph):
   rset = [(fromNode, toNode)] # return set (we assume it starts with this edge at least)
   print "function cutset: graph is ", graph
   graph.del_edge(fromNode, toNode)
   print "function cutset (2): graph is ", graph
   if not isGraphConnected(graph): # graphDivided()
      for each in graph.edges():
         print "each var is: ", each
         rset.extend(cutset(each[0],each[1],copy.copy(graph)))
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
      g.add_nodes([1,2,3])
      g.add_edge(1,2)
      g.add_edge(2,3)
      print "graph is ", g
      print cutset(1,2,g)

      # TODO: try pygraph.digraph(). for checking connectedness it should ignore direction.
      # for path finding, directionality does matter in a digraph.

if __name__ == '__main__':
   unittest.main()


