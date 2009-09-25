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
        #obj2.affixed must be afficed to the "surface" variable
        print "Agent.insert: pretending to look at the surface"
        print "Add the %s into the %s" % (object, into)
        return

class Plan(tinytree.Tree):
    pass

class Operation(Node):
    '''i made this so that i dont have to call functools.partial in a build method.
    >>> action1 = Operation(method="append", obj="a")
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
class Pie(Part, Plan): #or maybe Part should inherit from Plan?
    #def build(self, pie_name=None):
        #step 0. make the crust and slice the apples
        #step 1. affix pan to a surface
        #step 2. affix crust to the pan (don't do this in midair) #or it should be made in the pan
        #step 3. insert sliced apples into crust in the pan on the surface
        #step 4. detach the pan from the surface
        #step 5. bake the pan (and the food inside) into a mouth watering apple pie

    def build(self, pie_name=None):
        if pie_name is not None:
            #come up with some parameters by parsing pie_name
            self.crust = Crust() #another Part defined somewhere
            self.apples = Apples()
        else:
            #parameters were set in the __init__ or later
            pass

        #step 0. make the crust and slice the apples.
        crust = self.crust
        apples = self.apples
        crust.build()
        apples.build()

        #allocate a surface
        some_surface = Surface()
        some_surface.build()
        #TODO: a new surface is not necessary if you have a surface already
        #but it's possible that other recipes (say a biology lab protocol) will require a freshly sterilized and allocated surface

        #sterilize the surface (or should we assume all allocated items are sterilized?)
        sterilize = Operation("sterilize", object=some_surface)
        sterilized = Plan(objects=[some_surface], connector=sterilize)
        internal_steralize(some_surface) #pretend to do it

        #allocate a pan
        pan = CookingPan()
        pan.build()
        
        #sterilize the pan?

        #affix pan to the surface
        affix_pan_op = Operation("affix", object=pan, _to=sterilized)
        affixed_pan = Plan(objects=[pan, sterilized], connector=affix_pan_op)

        #a new pan is not necessary if you have the crust in one already
        def check_for_pan(crust):
            if crust.is_in(CookingPan): #er, how would this be done?
                return False
            else: return True
        the_conditional = functools.partial(check_for_pan, crust=crust)
        pan_the_crust = ConditionalOperation("insert", object=crust, into=affixed_pan, conditional=the_conditional)
        panned_crust = Plan(objects=[affixed_pan, crust], connector=pan_the_crust)
        #if the conditional is not met, the action will not be executed, however tree traversal can still occur

        #affix crust to the pan
        affix = Operation("affix", object=crust, _to=affixed_pan)
        affixed_crust = Plan(objects=[crust, affixed_pan], connector=affix)

        #TODO: apples may be in a container. make another ConditionalOperation
        
        #insert sliced apples into crust
        insert = Operation("insert", object=apples, into=crust)
        inserted = Plan(objects=[affixed_crust, apples], connector=insert)

        #bake the crust-and-apples into a mouth watering apple pie
        bake = Operation("bake", object=inserted, temperature="450 celsius", time="2 hr")
        #final step: turn self into a plan for a baked pie
        Plan.__init__(self, objects=[inserted], connector=bake)

        #you are now free to traverse this part and part plan

class TestInstructions(unittest.TestCase):
    def test_plan(self):
        #test that Part.build() makes the part into a plan
        pass
    def test_apple_pie(self):
        apple_pie = Pie("apple")
        apple_pie.build()
        steps = get_instructions(apple_pie, agent=Person())
        print steps
        #don't actually have a good test yet for this

