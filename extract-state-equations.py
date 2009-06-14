#!/usr/bin/python
# extract-state-equations.py
#
# Extract state equations for a mechanical assembly from a graph.
#
# Bryan Bishop (kanzure@gmail.com)
# http://heybryan.org/
# 2009-06-14

# cutset algorithm from Smári McCarthy.
#
# given edge e from edges E:
#	put nodes connected to e in separate bins.
#	for each node:
#		measure shortest distance to e.
# find which node of e that connection goes through, dump that vertex in relative bin.
# iff the path goes through no vertex currently residing in the /other/ bin.
#
# so you start by tossing the two start vertices into separate bins,
# then you walk the graph tossing vertices into bins until you've binned them all.
# then you run over all the pairs between the bins, and if there's an edge between them,
# then it's part of the set.
#
# given: a single edge.
# returned: the set of edges (including the given edge) that cut the graph into two parts.

# cycle algorithm.
#
# given a starting node (vertex), delete the edge pointing away from it, jump to where the edge was pointing.
# find the minimum path back to that original edge despite the deletion that was made in the graph.
#
# given: a single edge
# returns: all edges in the cycle that the original edge was a member of.





