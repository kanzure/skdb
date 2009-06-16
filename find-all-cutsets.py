#!/usr/bin/python
# Bryan Bishop (kanzure@gmail.com) http://heybryan.org/
# 2009-06-14
# find-all-cutsets.py - find all of the cutsets in a graph
import graph as pygraph # for pygraph 1.5
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
   #print "isGraphConnected: number of edges = ", len(graph.edges())
   if len(graph.edges()) == 0: # graph can't be connected with no edges
      return False
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
      


      # TODO: try pygraph.digraph(). for checking connectedness it should ignore direction.
      # for path finding, directionality does matter in a digraph.

if __name__ == '__main__':
   unittest.main()


