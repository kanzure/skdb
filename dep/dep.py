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
        #self.dependencies = []
        self.dependencysets = {}
    def __repr__(self):
        return ("%s, m:%s, approaches:%d" % (self.name, self.met, len(self.dependencysets)))
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
        if len(self.dependencysets) > 0:
            totallybroken = False
            for each in self.dependencysets:
                broken = False
                if len(self.dependencysets[each]) > 0:
                    for dependence in self.dependencysets[each]:
                        dependence.step()
                        if not dependence.met: broken = True
                if not broken: self.met = True # FIXME: keep track of which set of dependencies actually work
    def add_dependency(self, setname, dependency):
        # self depends on from1
        if self.dependencysets.has_key(setname):
            self.dependencysets[setname].append(dependency)
        else:
            self.dependencysets[setname] = [[dependency]]

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
    def add_dependency(self, setname, dependency, root):
        '''
        setname is the setname or index of to1's dependencyset list where this dependency is to be appended
        '''
        #from1.add_edge(from1, to1)
        root.add_dependency(setname, dependency)
        pygraph.digraph.add_edge(self, root, dependency) #dependency, root)

class TestResolver(unittest.TestCase):
    def test_Dependency(self):
        g = Resolver()
        fuel = Dependency(g,name="fuel")
        transportation = Dependency(g,name="transportation device")
        g.add_node(fuel)
        g.add_node(transportation)
        g.add_dependency("The Typical Approach", fuel, transportation)

        # a dependency of d1 is d2 (er, at least in name)
        self.assertTrue(g.dependencies((g.nodes())[0])==[fuel])
        print "grabbing the approaches to solving the 'transportation device': "
        print transportation.dependencysets

        print "\n\n\nyaml testing\n\n"
        print yaml.dump(g)
    def test_Resolver(self):
        pass

if __name__ == '__main__':
    unittest.main()
