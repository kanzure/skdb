#!/usr/bin/python
import unittest
from skdb.thirdparty.graphsynth import *

class TestGraphSynth(unittest.TestCase):
    def test_node(self):
        node = Node()
        self.assertTrue(len(node.arcs)==0)
    def test_arc(self):
        arc = Arc()
        self.assertTrue(arc._from == None)
        self.assertTrue(arc._to == None)
    def test_graph(self):
        graph = Graph()
        self.assertTrue(len(graph.nodes)==0)
        self.assertTrue(len(graph.arcs)==0)
        
        node = Node()
        graph.add_node(node)
        self.assertTrue(len(graph.nodes)==1)
        del node
        self.assertTrue(len(graph.nodes)==1) #is this right?
        arc = Arc()
        graph.add_arc(arc)
        self.assertTrue(len(graph.arcs)==1)
        del arc
        self.assertTrue(len(graph.arcs)==1)
        
        #graph.remove_node
        #graph.remove_arc

if __name__ == "__main__":
    unittest.main()

