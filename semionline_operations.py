import numpy as np
import networkx as nx
import math
from networkx.algorithms import bipartite
import random


DELTA_OPTIONS = [0, 0.2, 0.4, 0.6, 0.8, 1]

# Generates a networkx graph from a text file
# Input: text file 'file_name'
# Output: numpy array 'A', graph 'G'
def create_graph_from_text(file_name):
	f = open(file_name)
	n = int(f.readline())

	A = np.array([]).astype(int)
	for line in f:
		A = np.append(A, list(map(int, line.strip().split(" "))))
	A = np.array(A).reshape(n, n)

	G = nx.Graph()
	G.add_nodes_from(list(range(n)), bipartite=0, matched=False)
	G.add_nodes_from(list(range(n, n * 2)), bipartite=1, matched=False)
	for i in range(n):
		G.add_weighted_edges_from([(i, x, A[i][x - n])
								   for x in range(n, n * 2)])
	f.close()
	return A, G


# Computes the sum from the matching obtained
# Input: original array 'A', matching 'M'
# Output: sum of matching 'sum', zeros of A 'zeros'
def compute_sum_from_matching(A, M):
	n = A.shape[0]
	zeros = np.zeros([A.shape[0], A.shape[1]])
	sum = 0

	for i in range(n):
		sum = sum + A[i][M[i] - n]
		zeros[i][M[i] - n] = 1

	return sum, zeros


def create_subgraph_from_text(file_name, delta):
	f = open(file_name)
	n = int(f.readline())

	# Edges
	A = np.array([]).astype(int)
	for line in f:
		A = np.append(A, list(map(int, line.strip().split(" "))))
	A = np.array(A).reshape(n, n)

	# Subgraph
	known_percentage = 1 - delta
	count = math.floor(known_percentage * n)

	G = nx.Graph()
	G.add_nodes_from(list(range(n)), bipartite=0)
	G.add_nodes_from(list(range(n, n + count)), bipartite=1)
	for i in range(n):
		G.add_weighted_edges_from([(i, x, A[i][x - n])
								   for x in range(n, n + count)])
	f.close()
	return G


## Outputs (Cost of Semionline, Cost of Karp)
def semionline(fName, delta):
	A, G = create_graph_from_text(fName)

	# Offline Computation (Karp)
	M = bipartite.minimum_weight_full_matching(G)
	sumKarp = compute_sum_from_matching(A, M)			

	# Preprocessing
	subgraph = create_subgraph_from_text(fName, delta)
	lookup = bipartite.minimum_weight_full_matching(subgraph)

	# Semionline Matching
	semionline_matching = {}
	
	n = A.shape[0]
	for i in range(n):
		if i in lookup:
			# Matching already exists
			match = lookup[i]
			semionline_matching[i] = match
			
			G.nodes[i]["matched"] = True
			G.nodes[match]["matched"] = True
		else:
			# Randomized Greedy Algorithm --> Needs to be improved

			print("Node: ", i)
			match = get_closest(G, A[i])
			semionline_matching[i] = match

			print("Match: ", match)

			G.nodes[i]["matched"] = True
			G.nodes[match]["matched"] = True
	

	for i in range(2 * n):
		print(G.nodes[i]["matched"])

	sumSemionline = compute_sum_from_matching(A, semionline_matching)
	return sumSemionline[0], sumKarp[0]



## Sorts edges in the following format:
## {weight: [edge1, edge2, ...]}
def sort_edges(edges):
	out = {}
	for i in range(1, 101):
		for j in range(len(edges)):
			if edges[j] == i:
				if not i in out:
					out[i] = []	
				out[i].append(j)
	return out


## Returns nearest node. In case of multiple closest nodes, chooses randomly
def get_closest(graph, edges):
	sorted_edges = sort_edges(edges)
	n = edges.shape[0]

	print(sorted_edges)

	for key in sorted(sorted_edges.keys()):
		# for node in sorted_edges[key]:
		# 	if not graph.nodes[n + node]["matched"]:
		# 		return n + node
		choices = get_unmatched(graph, sorted_edges[key], n)		## TODO: Fix this
		if choices:
			choice = random.choice(choices)
			return n + choice


## Returns list of unmatched nodes, if any
def get_unmatched(graph, nodes, n):
	for node in nodes:
		if graph.nodes[n + node]["matched"]:
			nodes.remove(node)
	return nodes


for i in range(2):
	delta = DELTA_OPTIONS[i]
	print("Delta: ", delta)

	ALG, OPT = semionline("test/assign300.txt", delta)

	print(ALG, "/", OPT)
	print("c: ", ALG / OPT, "\n")
# print(sum)