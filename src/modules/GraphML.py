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


	## Uses a modified perturbation method (Kasilag et al, 2022) to get a predicted matching
	## Input: proportion of unknown 'delta': range(0.0-1.0), proportion of perturbed 'epsilon': range(0.0-1.0), perturb amount 'k'
	## Output: copy of self.graph with modified edge weights
	def generate_perturbed_graph(self, delta, epsilon, k):
		# Get elements to perturb
		RHS_count = math.floor(delta * self.n)													## WRONG -> delta IS the unknown part to perturb
		RHS_candidates = np.random.choice(range(self.n, 2 * self.n), RHS_count, replace=False)

		# Generate perturbation candidates
		perturb_candidates = []
		for u in range(self.n):
			for v in RHS_candidates:
				edge_index = u * self.n + (v - self.n)
				perturb_candidates.append(edge_index)
		
		# Get elements to perturb
		perturb_count = math.floor(epsilon * len(perturb_candidates))
		perturb_indices = np.random.choice(perturb_candidates, perturb_count, replace=False)
		
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


	## Converts an edge index to it's corresponding u, v nodes
	## Input: edge_index: range(self.n^2)
	## Output: node indices (u, v)
	def edge2nodes(self, edge_index):
		if edge_index < 0 or edge_index >= self.n * self.n:
			raise Exception(f"{Fore.RED}Edge index out of bounds!{Fore.WHITE}")

		u = edge_index // self.n
		v = (edge_index % self.n) + self.n		# Note: v is offset by self.n
		return u, v


	## Gets the root mean squared deviation of a graph compared to self.graph
	## Input: deviated graph
	## Output: RMSD
	def calculate_rmsd(self, deviated_graph: nx.Graph):
		summation = 0
		for u in range(self.n):
			for v in range(self.n, 2 * self.n):
				deviation = self.graph.edges[u, v]["weight"] - deviated_graph.edges[u, v]["weight"]
				summation += deviation ** 2

		return math.sqrt(summation / self.n ** 2)