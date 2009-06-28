#!/usr/bin/python
# hierarchical dependency resolution system
# Bryan Bishop kanzure@gmail.com http://heybryan.org/
# 2009-06-27

import graph as pygraph
import unittest
import yaml

# node class
class Dependency(yaml.YAMLObject):
    def __init__(self, graph, name="dependency name here"):
        self.name = name
        self.graph = graph
        self.met = False
        self.dependencies = []
        #self.dependencysets = []
    def __repr__(self):
        return ("%s, s:%s" % (self.name, self.met))
    def solved(self):
        # note: if all dependencies of this dependency are solved,
        # then this dependency should be by definition 'solved'.
        # FIXME: check for whether or not all dependencies are solved.
        return self.met
    #def dependencies(self):
    #    return self.neighbors()
    def step(self):
        # note: if all dependencies of this dependency are solved,
        # then this dependency should be by definition 'solved'.
        # check whether or not all of the dependencies are solved
        if len(self.dependencies) > 0:
            broken = False
            for each in self.dependencies: #for each in g.dependencies(self):
                each.step()
                if not (each.met):
                    broken = True
            if not broken: self.met = True
    def add_edge(self, from1):
        # self depends on from1
        self.dependencies.append(from1)

class Resolver(yaml.YAMLObject, pygraph.digraph):
    def __init__(self):
        self.node_neighbors = {}
        self.node_incidence = {}
        self.node_attr = {}
        self.edge_properties = {}
        self.edge_attr = {}
        return
    def run(self):
        for each in self.nodes():
            each.step()
    def dependencies(self,node):
        return self.neighbors(node)
    def unmets(self,node):
        # return unmet dependencies
        return
    def add_edge(self, from1, to1):
        #from1.add_edge(from1, to1)
        to1.add_edge(from1)
        pygraph.digraph.add_edge(self, from1, to1)

class TestResolver(unittest.TestCase):
    def test_Dependency(self):
        g = Resolver()
        d1 = Dependency(g,name="transportation device")
        d2 = Dependency(g,name="fuel")
        g.add_node(d1)
        g.add_node(d2)
        g.add_edge(d1,d2)

        # a dependency of d1 is d2 (er, at least in name)
        self.assertTrue(g.dependencies((g.nodes())[1])==[d2])
        print g.dependencies((g.nodes())[1])
    def test_Resolver(self):
        pass

if __name__ == '__main__':
    unittest.main()
