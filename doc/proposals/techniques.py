#!/usr/bin/python
from copy import copy, deepcopy
from skdb.core.yamlcrap import *
from skdb import Unit, Vector, Process, load_package
import unittest

class Human:
    '''a human is someone who might want to follow some instructions'''
    def align(self, interface1, interface2):
        return Step("align interface %s along the mating axis defined by interface %s" % (interface2.name, interface1.name))
    def push(self, object=None, force=None, vector=None):
        return Step("push %s with %s along %s" % (object.name, force, vector))

class Robot:
    '''a robot is something that might want to follow some instructions'''
    def align(self, interface1, interface2):
        pass

class Step(FennObject, str):
    yaml_tag="!step"

class Instructions(FennObject, list):
    yaml_tag="!instructions"
    
class Fit(Process):
    yaml_tag="!fit"

class Press(Fit):
    '''!press *part1interface1 *part2interface34'''
    yaml_tag="!press"
    def __init__(self, option):
        self.interface1 = option.interface1
        self.interface2 = option.interface2
    def options(self, interface1, interface2):
        '''figures out press fit options between two given part interfaces'''
        pass
    def __repr__(self):
        pass
    def instructions(self, tool):
        '''generate instructions for using this technique with a particular tool'''
        #technically you should be able to use more than one tool
        steps = Instructions() #it's essentially a list
        step1 = tool.align(self.interface1, self.interface2) #with the tool "tool", align interface1 and interface2 (with their vectors)
        steps.append(step1)
        step2 = tool.push(object=self.interface1, force=Unit("10 N"), vector=Vector(0,1,0)) #normal_to(self.interface2)))
        steps.append(step2)
        return steps

class TestPressFitTechnique(unittest.TestCase):
    def test_press(self):
        lego_pack = load_package("lego")
        lego_pack.load_data()
        part1 = deepcopy(lego_pack.parts[0])
        part2 = deepcopy(lego_pack.parts[0])
        options = part1.options(part2)
        option1 = options[1]
        press = Press(option1) #is this a valid operation? this is determined by whether or not it is meaningful.
        tool = Human()
        #tool = Robot()
        steps = press.instructions(tool)
        print steps

if __name__ == "__main__":
    unittest.main()

