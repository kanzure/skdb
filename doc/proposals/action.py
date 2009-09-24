#!/usr/bin/python
#this code doesn't work
#fenn and kanzure were shooting the breeze one day
#and then this happened :(
from skdb import FennObject

class Agent:
    def insert(self, object=None, into=None, surface=None):
        '''insert the subject into the _into'''
        #obj2.affixed must be afficed to the "surface" variable
        print "Agent.insert: pretending to look at the surface"
        print "Add the %s into the %s" % (object, into)
        return

class Tree(FennObject):
    pass

class State:
    def merge(self, other):
    '''merge two states together'''
        for element in other:
            if element in self: break
            else: self.add(element)

class FakeAction(Edge):
    '''i made this so that i dont have to call functools.partial in a build method.
    >>> action1 = FakeAction(method="append", obj="a")
    >>> #later you want to actually do this action
    >>> action1.do(agent=Human())
    '''
    def __init__(self, method="error", **keywords):
        '''somehow store the keyword arguments please'''
        pass
    def do(self, agent=Agent()):
        '''looks for self.method in agent.__dict__.keys() and then calls it with the right parameters'''
        pass

class Pie(Part):
    '''Pie is in the Pie package'''
    def build(self, agent=Agent()):
        '''builds a pie'''
        resulting_tree = Tree()

        #note that the PiePackage depends on Crust and Apple (in the non-existant metadata)
        crust = Crust("standard crust")
        crust_tree = crust.build()
        crust_state = crust_tree.latest_state
        apples = Apple("green")
        apple_tree = apples.build()
        apples_state = apple_tree.latest_state #should contain our apple

        #add these two trees into the resulting tree
        resulting_tree.add(crust_tree)
        resulting_tree.add(apple_tree)
        #(they should be disconnected at the moment)

        merged_state = State()
        merged_state.merge(apples_state)
        merged_state.merge(crust_state)

        agent.affix(object=crust, state=crust_state)
        agent.insert(object=apples, into=crust, state=merged_state)

        new_node = Node()
        #silently remove crust and apples from the state, and add a pie (while he wasn't looking)
        merged_state.remove(apples)
        merged_state.remove(crust)
        merged_state.add(Pie(crust=crust, apples=apples))
        new_node.state = merged_state

        #new_node.state = copy(self)
        #make an ordered list (python does this by default, so maybe we need a way to let it be unordered if that's ok?)
        new_node.add_edge(action1, _from=crust_tree)
        new_node.add_edge(action2, _from=apple_tree)
        resulting_tree.add_node(new_node)

        return resulting_tree

