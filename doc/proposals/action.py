#!/usr/bin/python
#this code doesn't work
#fenn and kanzure were shooting the breeze one day
#and then this happened :(

from skdb import FennObject
import tinytree #use graphsynth.Graph instead?
import unittest

#boring stuff, setting up the problem
class Agent:
    def insert(self, object=None, into=None, surface=None):
        '''insert the subject into the _into'''
        #obj2.affixed must be afficed to the "surface" variable
        print "Agent.insert: pretending to look at the surface"
        print "Add the %s into the %s" % (object, into)
        return

class Tree(tinytree.Tree):
    pass

class ActionContainer(Node):
    '''i made this so that i dont have to call functools.partial in a build method.
    >>> action1 = ActionContainer(method="append", obj="a")
    >>> #later you want to actually do this action
    >>> action1.do(agent=Human())
    '''
    def __init__(self, method="error", **keywords):
        '''somehow store the keyword arguments please'''
        self.method =method
        pass
    def do(self, agent=Agent()):
        '''looks for self.method in agent.__dict__.keys() and then calls it with the right parameters'''
        pass

#meanwhile somewhere in the pie package..
class Pie(Part, Tree): #or maybe Part should inherit from Tree?
                       #but isn't a Part also an Assembly or Graph?
    def build(self, pie_name=None):
        #first we look at pie_name and come up with a pie if it's there
        if pie_name is not None:
            #come up with some parameters by parsing pie_name
            self.crust = Crust() #another Part defined somewhere
            self.apples = Apples()

        #step 0. make the crust and slice the apples.
        crust = self.crust
        apples = self.apples
        crust.build()
        apples.build()

        #step 1. affix crust to some surface (don't do this in midair)
        surface1 = Surface()
        affix = ActionContainer("affix", object=crust, _to=surface1)
        affixed_crust = Tree(objects=[crust, surface1], connector=affix)

        #step 2. insert sliced apples into crust
        insert = ActionContainer("insert", object=apples, into=crust)
        inserted = Tree(objects=[affixed_crust, apples], connector=insert)

        #step 3. bake the crust-and-apples into a mouth watering apple pie
        bake = ActionContainer("bake", object=inserted, temperature="450 celsius", time="2 hr")
        #finally we set "self" to be this baked pie
        Tree.__init__(self, objects=[inserted], connector=bake)

        #you are now free to traverse this tree/part

class TestInstructions(unittest.TestCase):
    def test_tree(self):
        #test that Part.build() makes the part into a tree
        pass
    def test_apple_pie(self):
        apple_pie = Pie("apple")
        apple_pie.build()
        steps = get_instructions(apple_pie, agent=Person())
        print steps
        #don't actually have a good test yet for this

