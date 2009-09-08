#!/usr/bin/python
import unittest
import yaml
from skdb.core import dep

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
    def test_dependency_again(self):
        #say we don't have skdb.packages.screw or are not aware of it.
        screw1 = skdb.pymates.Part(name="screw")
        #choose from these: threading, thread rolling, thread milling, thread whirling
        dependency_set_build = skdb.dep.dependency_set(type="options")
        dependency_set_build.add("threading")
        dependency_set_build.add("thread rolling")
        dependency_set_build.add("thread milling")
        dependency_set_build.add("thread whirling")
        screw1.dependencies.add(type="build",set=dependency_set_build)
        dependency_set_build2 = skdb.dep.dependency_set(type="options")

    def test_Resolver(self):
        pass

if __name__ == '__main__':
    unittest.main()
