#!/usr/bin/python
import unittest
import yaml
import dep

class TestResolver(unittest.TestCase):
    def test_Dependency(self):
        g = dep.Resolver()
        fuel = dep.Dependency(g,name="fuel")
        transportation = dep.Dependency(g,name="transportation device")
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
