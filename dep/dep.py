#!/usr/bin/python
# hierarchical dependency resolution system
# Bryan Bishop kanzure@gmail.com http://heybryan.org/
# 2009-06-27

import graph as pygraph
import unittest

# node class
class Dependency:
    def __init__(self, name="dependency name here"):
        self.name = name
    def __repr__(self):
        return self.name
    #def dependencies(self):
    #    return self.neighbors()

class Resolver(pygraph.digraph):
    def __init__(self):
        self.node_neighbors = {}
        self.node_incidence = {}
        self.node_attr = {}
        self.edge_properties = {}
        self.edge_attr = {}
        return
    def dependencies(self,node):
        return self.neighbors(node)

class TestResolver(unittest.TestCase):
    def test_Dependency(self):
        g = Resolver()
        d1 = Dependency(name="transportation device")
        d2 = Dependency(name="fuel")
        g.add_node(d1)
        g.add_node(d2)
        g.add_edge(d1,d2)

        # a dependency on d1 is d2 (er, at least in name)
        self.assertTrue(g.dependencies((g.nodes())[1])==[d2])

    def test_Resolver(self):
        pass

if __name__ == '__main__':
    unittest.main()
