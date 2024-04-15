import math
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
from .ProgressBar import ProgressBar

## Graph for use in the Assignment Problem
## Has functions to aid in semi-online matching
class GraphAP:
	def __init__(self, file_path):
		self._create_from_file(file_path)


	## Initializes graph variables from a file
	## Input: relative path 'rel_path'
	def _create_from_file(self, file_path):
		# Open the file
		f = open(file_path)

		# Group the raw weights in a 2D array
		# weights[u][v] -> weight of edge between u(LHS) and v(RHS)
		n = int(f.readline())
		weights = np.array([]).astype(int)

		# Initialize progress bar
		print("Processing file...")
		with open(file_path, "rb") as f_temp:
			progress_total = sum([1 for _ in f_temp]) - 1
		line_count = 0
		progress_bar = ProgressBar(progress_total) 
		progress_bar.update_and_display(0)

		for line in f:
			weights = np.append(weights, list(map(int, line.strip().split(" "))))
			
			# Progress bar
			line_count += 1
			progress_bar.update_and_display(line_count)

		weights = np.array(weights).reshape(n, n) 

		f.close()

		# Create NetworkX Graph and the sorted_edges
		graph = nx.Graph()
		sorted_edges = np.empty(2 * n, dtype=dict)
		for i in range(2 * n):
			sorted_edges[i] = {}

		graph.add_nodes_from(list(range(n)), bipartite=0, matched=False)
		graph.add_nodes_from(list(range(n, n * 2)), bipartite=1, matched=False)
		
		# Initialize progress bar
		print("Building graph...")
		progress_total = n * n
		progress_bar = ProgressBar(progress_total) 
		progress_bar.update_and_display(0)

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

				# Progress bar
				progress_bar.update_and_display(u * n + (v - n) + 1)


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


	## Creates a lookup table from the first 1 - δ % of RHS nodes
	## Input: proportion of unknown 'delta': range(0.0-1.0), RHS toggle 'rhs'
	## Output: one-way matching dictionary with RHS nodes as keys by default
	def generate_lookup_table(self, delta, rhs=True):
		# Creates a reduced subgraph
		cull_count = math.floor(delta * self.n)

		if cull_count == self.n:
			# Returns an empty lookup table if all nodes are unknown
			return {}

		# cull_indices = list(range(2 * self.n - cull_count, 2 * self.n))	<-- Alternative: Culls the last x nodes 
		cull_indices = np.random.choice(range(self.n, 2 * self.n), cull_count, replace=False)

		subgraph = self.graph.copy()
		subgraph.remove_nodes_from(cull_indices)

		return GraphAP.get_offline_matching(subgraph, rhs)


	## Returns an optimal offline matching using Karp algorithm
	## Output: one-way matching dictionary (RHS keys)
	def get_offline_matching(graph, rhs=True):
		matching = bipartite.minimum_weight_full_matching(graph)
		return GraphAP.convert_to_oneway_matching(matching, rhs)


	## Static Function: Halves the size of a two-way matching
	## Input: bloated matching 'matching', RHS toggle 'rhs'
	## Ouptut one-way matching
	def convert_to_oneway_matching(matching, rhs=True):
		count = int(len(matching.items()) / 2) 

		if rhs:
			true_matching = list(matching.items())[count:]
		else:
			true_matching = list(matching.items())[:count]

		return {u:v for u, v in true_matching}

	
	## Returns the sum of a matching (works for incomplete matches)
	## Input: 'matching': dict, bloated toggle 'bloated'
	## Note: a matching is bloated if it contains matches from both directions
	def get_projected_matching_sum(self, matching, bloated=False):
		if bloated:
			count = int(len(matching.items()) / 2) 
			true_matching = list(matching.items())[:count]
		else:
			true_matching = list(matching.items())

		weights = [self.graph.edges[u, v]["weight"] for u, v in true_matching]
		return sum(weights)


	## Resets the graph's attributes to allow reuse
	def flush(self):
		# Sets all nodes to unmatched
		for i in range(2 * self.n):
			self.graph.nodes[i]["matched"] = False

	
	## Sets the nodes of an edge to matched
	def set_matched(self, u, v):
		self.graph.nodes[u]["matched"] = True
		self.graph.nodes[v]["matched"] = True
		
	
	## Randomly chooses the closest unmatched node (Works for both LHS and RHS)
	## Input: node index 'i'
	## Output: matched node index
	def get_closest(self, i):
		edges = self.sorted_edges[i]

		for w in edges.keys():
			# Scans for closest unmatched nodes
			unmatched = edges[w].copy()
			
			for j in range(len(unmatched)-1, -1, -1):
				node_index = unmatched[j]
				if self.graph.nodes[node_index]["matched"]:
					unmatched.remove(node_index)

			# Chooses randomly from the unmatched nodes
			if unmatched:
				choice = np.random.choice(unmatched)
				return choice

		print(f"Error: match for node {i} not found!")
		