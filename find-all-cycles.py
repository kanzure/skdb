#!/usr/bin/python
# http://www2.decf.berkeley.edu/~faridani/python.htm
# TODO: convert to python-graph instead of silly adjacency matrix thingy.
import pygraph
import random
from sets import Set
import copy

graph = {'1': ['2', '4','5'],
             '2': ['1', '3','5'],
             '3': ['2','5','6'],
             '4': ['1','7','5'],
             '5': ['1','2','3', '4','6','7','8','9'],
             '6': ['3','5','9'],
             '7': ['4','5','8'],
             '8': ['7','5','9'],
             '9': ['8','5','6']}

def find_all_paths(graph, start, end, path=[]):
        #http://www.python.org/doc/essays/graphs/
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_node(start):
            return []
        paths = []
        #print "current path is: ", path
        for node in graph.neighbors(start):
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

def find_cycle(graph):
    cycles=[]
    for startnode in graph.nodes():
        for endnode in graph.nodes():
            newpaths = find_all_paths(graph, startnode, endnode)
            for path in newpaths:
               if len(path)>2:
                  if path[0] in graph.neighbors(path[len(path)-1]):
                     path.append(path[0])
                     cycles.append(path)
                #if(len(path)>2):
                #  path.append(path[0])
                #  cycles.append(path)
                #if (len(path)==len(graph)):
                #    if path[0] in graph.neighbors(path[len(graph)-1]):
                #        #print path[0], graph[path[len(graph)-1]]
                #        path.append(path[0])
                #        cycles.append(path)
    return cycles

# Set(A).intersection(B) == len(A) and len(A) == len(B)
# [[16, 17, 18, 13, 14, 15, 16], [18, 13, 14, 15, 16, 17, 18]]
def reduceCycles(cycles):
   for cycle in cycles:
      for ocycle in cycles:
         match = False
         if (len(cycle) == len(ocycle)) and not (cycle == ocycle): # if they have the same path lengths
            print "set intersection is: ", Set(cycle).intersection(ocycle), " and length is: ", len(Set(cycle).intersection(ocycle))
            if (len(Set(cycle).intersection(ocycle)) == len(cycle)-1): # note that the cycle has an extra node in it (the last node in the path)
               # they are the same cycle. blasphemy!
               match = True
         if match:
            print "match between:\n\t", cycle, "\n\t", ocycle, "\n\n"
            cycles.remove(ocycle)
   return cycles 

def doReduction(cycles):
   oldcycles = copy.copy(cycles)
   if(len(cycles) > 0):
      while(len(cycles) == len(oldcycles)):
         cycles = reduceCycles(cycles)
   return cycles


## this seems to be fixed.
#blah = reduceCycles([[16, 17, 18, 13, 14, 15, 16], [18, 13, 14, 15, 16, 17, 18]])
#print blah
#exit()

g = pygraph.digraph()
graphsize = random.randint(2,20)
g.add_nodes(range(1,graphsize+1))
for i in range(1,graphsize):
   g.add_edge(i,i+1)
# now let's make cycles by adding edges.
redges = random.randint(1,5)
for i in range(1,redges+1):
   A = random.randint(1,graphsize)
   B = random.randint(1,graphsize)
   # note: it's kind of useless if A = B or if B=A+1.
   if (not (A == B or B==A+1)):
      g.add_edge(A,B)
      print "fake edge between ", A, " and ", B
#g.add_edge(3,1)
#g.add_edge(4,1)
cycles = find_cycle(g)
print "there is an edge between successive numerical nodes.\nthere are ", redges, " other edges in the system.\n"
print g
print cycles

newstuff = doReduction(cycles)
print newstuff

exit()


oldcycles = copy.copy(cycles)
reduced = reduceCycles(cycles)
print "the original set of cycles:\n", oldcycles
print "and now for the reduced set of cycles:\n", reduced
print "going for another round of reduction ...\n\n\n"
oldreduced = copy.copy(reduced)
reducedagain = reduceCycles(reduced)
print "the original graph:\n", g
print "the original set of cycles:\n", oldcycles
print "the reduced set of cycles:\n", oldreduced
print "the doubly reduced set of cycles:\n", reducedagain
# eek. too many redundant paths.







def find_paths(graph):
    cycles=[]
    for startnode in graph:
        for endnode in graph:
            newpaths = find_all_paths(graph, startnode, endnode)
            for path in newpaths:
                if (len(path)==len(graph)):                    
                    cycles.append(path)
    return cycles


