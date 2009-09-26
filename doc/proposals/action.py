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
    def do(self, method=None):
        method()

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
    def build(self, pie_name=None):
        if pie_name is not None:
            #come up with some parameters by parsing pie_name
            self.crust = Crust() #another Part defined somewhere
            self.apples = Apples()
        else:
            #parameters were set in the __init__ or later
            pass

        #make the crust and slice the apples.
        crust = self.crust
        apples = self.apples
        crust.build()
        apples.build()

        #build a new surface
        some_surface = Surface()
        some_surface.build()

        #sterilize the surface (or should we assume all allocated items are sterilized?)
        sterilize_surface_op = Operation(action="sterilize", object=some_surface)
        sterilized_surface = Plan(objects=[some_surface], connector=sterilize_surface_op)

        #a new surface is not necessary if you can allocate one
        def autofalse():
            return False
        get_a_surface = Operation(action="allocate", object=some_surface, conditional=autofalse) #not sure how to alloc :(
        some_surface = Plan(connector=get_a_surface, substitutes=[sterilized_surface])
        #if get_a_surface's conditional == False, some_surface will just secretly point to sterilized_surface (a fresh build)

        #build a new pan
        pan = CookingPan()
        pan.build()
        
        #sterilize the pan
        sterilize_pan_op = Operation(action="sterilize", object=pan)
        sterilized_pan = Plan(objects=[pan], connector=sterilize_pan_op)

        #a new pan is not necessary if you can allocate one
        get_a_pan = Operation(action="allocate", object=pan, conditional=autofalse)
        some_pan = Plan(connector=get_a_pan, substitutes=[sterilized_pan])
        #if get_a_pan's conditional == False, some_plan will just secretly point to sterilized_pan

        #affix pan to the surface
        affix_pan_op = Operation(action="affix", object=some_pan, _to=sterilized_surface)
        affixed_pan = Plan(objects=[some_pan, sterilized_surface], connector=affix_pan_op)

        #a new pan is not necessary if you have the crust in one already
        def check_for_pan(crust):
            if crust.is_in(CookingPan): #how?
                return False
            else: return True
        the_conditional = functools.partial(check_for_pan, crust=crust)
        pan_the_crust = Operation(action="insert", object=crust, into=affixed_pan, conditional=the_conditional)
        panned_crust = Plan(objects=[affixed_pan, crust], connector=pan_the_crust, substitutes=[crust])
        #if the conditional is not met, the action will not be executed, however tree traversal can still occur
        #substitutes=[crust] simply means that if the Operation doesn't execute, what to go try instead
        #otherwise the "affixed pan" would be used when it's not needed, you already have a panned_crust apparently

        #if the apples are in a container, remove them from the container
        def check_for_container(object):
            if object.is_in(Container): #any ideas?
                return True
            return False
        apples_in_container = functools.partial(check_for_container, object=apples)
        remove_apples_op = Operation(action="remove_container", object=apples, conditional=apples_in_container)
        removed_apples = Plan(objects=[apples], connector=remove_apples_op) #in this case the substitute is unambiguous (apples)
        
        #slice the apples if they aren't sliced
        def are_apples_sliced_checker(apples):
            return apples.sliced #any better ideas?
        are_apples_sliced = functools.partial(are_apples_sliced_checker, apples=removed_apples) 
        slice_apples_op = Operation(action="slice", object=removed_apples, conditional=are_apples_sliced)
        sliced_apples = Plan(objects=[removed_apples], connector=slice_apples_op) #in this case the substitute is unambiguous (removed_apples)

        #insert sliced apples into crust
        insert = Operation(action="insert", object=removed_apples, into=panned_crust)
        inserted = Plan(objects=[panned_crust, removed_apples], connector=insert)

        #build an oven
        oven = Oven()
        oven.build()

        #new oven not necessary if you can allocate one
        get_an_oven = Operation(action="allocate", object=oven, conditional=autofalse)
        some_oven = Plan(connector=get_an_oven, substitutes=[oven])
        #if get_an_oven's conditional == False, some_oven will just secretly point to oven

        #bake the crust-and-apples into a mouth watering apple pie via the oven
        bake = Operation(action="bake", object=inserted, temperature="450 celsius", time="36 hr", device=some_oven)
        #final step: turn self into a plan for a baked pie
        Plan.__init__(self, objects=[inserted, some_oven], connector=bake)

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

