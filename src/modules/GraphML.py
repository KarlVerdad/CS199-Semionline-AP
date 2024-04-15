import math
import numpy as np
import networkx as nx
from colorama import Fore
from .GraphAP import GraphAP

## Kasilag's version of the Online AP with ML Advice
class GraphML(GraphAP):
	def __init__(self, file_path):
		super().__init__(file_path)

		## Gets the minimum and maximum edge weights from the graph
		max = 1
		min = 100

		for u in range(self.n):
			for v in range(self.n, 2 * self.n):
				weight = self.graph.edges[u, v]["weight"]
				if weight > max:
					max = weight
				if weight < min:
					min = weight

		self.max = max
		self.min = min


	## Uses the perturbation method (Kasilag et al, 2022) to get a predicted matching
	## Input: proportion of perturbed 'e': range(0.0-1.0), perturb amount 'k'
	## Output: copy of self.graph with modified edge weights
	def generate_perturbed_graph(self, e, k):
		perturb_count = math.floor(e * self.n * self.n)
		perturb_indices = np.random.choice(range(self.n * self.n), perturb_count, replace=False)
		
		# Perturbation
		subgraph = self.graph.copy()
		for i in perturb_indices:
			u, v = self.edge2nodes(i)
			weight = subgraph.edges[u, v]["weight"]

			if weight - k < self.min:
				perturbation = k
			elif weight + k > self.max:
				perturbation = -k
			else:
				if np.random.choice([True, False]):
					perturbation = k
				else:
					perturbation = -k
			subgraph.edges[u, v]["weight"] += perturbation
		return subgraph


	## Converts an edge index (range(self.n^2)) to it's corresponding u, v nodes
	def edge2nodes(self, edge_index):
		if edge_index < 0 or edge_index >= self.n * self.n:
			raise Exception(f"{Fore.RED}Edge index out of bounds!{Fore.WHITE}")

		u = edge_index // self.n
		v = (edge_index % self.n) + self.n		# Note: v is offset by self.n
		return u, v
