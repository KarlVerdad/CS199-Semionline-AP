import os
import math
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite


## Graph for use in the Assignment Problem
## Has functions to aid in semi-online matching
class GraphAP:
	def __init__(self, rel_path):
		self._create_from_file(rel_path)


	## Initializes graph variables from a file
	## Input: relative path 'rel_path'
	def _create_from_file(self, rel_path):
		# Open the file
		dir = os.path.dirname(__file__)
		file_path = os.path.join(dir, rel_path)
		f = open(file_path)

		# Group the raw weights in a 2D array
		# weights[u][v] -> weight of edge between u(LHS) and v(RHS)
		n = int(f.readline())
		weights = np.array([]).astype(int)
		for line in f:
			weights = np.append(weights, list(map(int, line.strip().split(" "))))
		weights = np.array(weights).reshape(n, n) 

		f.close()

		# Create NetworkX Graph and the sorted_edges
		graph = nx.Graph()
		sorted_edges = np.empty(2 * n, dtype=dict)
		for i in range(2 * n):
			sorted_edges[i] = {}

		graph.add_nodes_from(list(range(n)), bipartite=0, matched=False)
		graph.add_nodes_from(list(range(n, n * 2)), bipartite=1, matched=False)
		for u in range(n):
			for v in range(n, 2 * n):
				# Adds edge to Graph
				w = weights[u][v - n]
				graph.add_edge(u, v, weight=w)
				
				# Initialize sorted_edges array if necessary
				if not w in sorted_edges[u]:
					sorted_edges[u][w] = []
				if not w in sorted_edges[v]:
					sorted_edges[v][w] = []
				
				# Adds connected node to sorted_edges
				sorted_edges[u][w].append(v)
				sorted_edges[v][w].append(u)

		# Sorts the items of sorted_edges
		for i in range(2 * n):
			sorted_edges[i] = dict(sorted(sorted_edges[i].items()))

		# Assign class variables
		self.n = n
		self.graph = graph
		self.sorted_edges = sorted_edges


	## Validator to check if all the nodes have a match
	## Output: bool
	def is_matched_completely(self):
		for i in range(2 * self.n):
			is_matched = self.graph.nodes[i]["matched"]
			if not is_matched:
				return False
		return True


	## Creates a lookup table from the first 1 - δ proportion of RHS nodes
	## Input: proportion of unknown 'delta': range(0.0-1.0), RHS toggle 'rhs'
	## Output: one-way matching dictionary with RHS nodes as keys by default
	def generate_lookup_table(self, delta, rhs=True):
		# Creates a reduced subgraph
		cull_count = math.floor(delta * self.n)
		if cull_count == self.n:
			# Returns an empty lookup table if all nodes are unknown
			return {}

		cull_indices = list(range(2 * self.n - cull_count, 2 * self.n))

		subgraph = self.graph.copy()
		subgraph.remove_nodes_from(cull_indices)

		# Halves the items in the matching to remove duplicate weights
		matching = bipartite.minimum_weight_full_matching(subgraph)
		count = int(len(matching.items()) / 2) 

		if rhs:
			true_matching = list(matching.items())[count:]
		else:
			true_matching = list(matching.items())[:count]

		return {u:v for u, v in true_matching}

	
	## Returns the sum of a matching (works for incomplete matches)
	## Input: 'matching': dict, bloated toggle 'bloated'
	## Note: a matching is bloated if it contains matches from both directions
	def get_matching_sum(self, matching, bloated=False):
		if bloated:
			count = int(len(matching.items()) / 2) 
			true_matching = list(matching.items())[:count]
		else:
			true_matching = list(matching.items())

		weights = [self.graph.edges[u, v]["weight"] for u, v in true_matching]
		return sum(weights)



foo = GraphAP("../../test/assign200.txt")

for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
	lookup = foo.generate_lookup_table(i, rhs=True)
	print(lookup)
	foo.get_matching_sum(lookup)
	print(foo.get_matching_sum(lookup))