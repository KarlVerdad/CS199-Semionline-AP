import os
import argparse
import numpy as np
import networkx as nx
from colorama import Fore
from modules.GraphML import GraphML


VALID_EXT = ('.txt')		# Valid input file extensions
EPSILON_OPTIONS = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
K_OPTIONS = [10, 30, 50]


def simulate_onlineML(G: GraphML, seed=238974):
	print(f"=== n: {G.n}, seed: {seed} ===")

	# Offline matching (Karp)
	karp_matching = GraphML.get_optimal_matching(G.graph)
	karp_sum = G.get_projected_matching_sum(karp_matching)

	print(f"Karp: {karp_sum}")

	# Online matching with simulated ML
	competitive_ratio_results = []
	for e in EPSILON_OPTIONS:
		for k in K_OPTIONS:
			# np.random.seed(seed)

			predicted_graph = G.generate_perturbed_graph(e, k)
			predicted_matching = GraphML.get_optimal_matching(predicted_graph)
			predicted_sum = G.get_projected_matching_sum(predicted_matching)

			# Consolidate Results
			empirical_competitive_ratio = predicted_sum / karp_sum
			data = (e, k, empirical_competitive_ratio)
			competitive_ratio_results.append(data)

			# Display results
			print(f"ε: {e:.2f} | k: {k}")
			print(predicted_sum, "/", karp_sum)
			print(empirical_competitive_ratio)

	# Display summarized results
	print(f"===Summary===")
	summarized_results = [(round(e, 3), k, round(c, 3)) for e, k, c in competitive_ratio_results]
	print("ε\tk\tEmpirical C. Ratio")
	for e, k, c in summarized_results:
		print(f"{e}\t{k}\t{c}")

	return competitive_ratio_results


if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("path", help="Directory/File to use as input")

	args = parser.parse_args()

	# Process arguments
	input_files = []
	path = os.path.abspath(args.path)
	if os.path.isfile(path):
		# Path argument is a file
		input_files.append(path)
	elif os.path.isdir(path):
		# Path argument is a directory
		for file in sorted(os.listdir(path)):
			if file.endswith(VALID_EXT):
				file_path = os.path.join(path, file)
				input_files.append(file_path)
	else:
		raise Exception(f"{Fore.RED}Invalid path argument!{Fore.WHITE}")


	# Run simulations
	for file in input_files:
		print(f"=== File: {os.path.basename(file)} ===")
		G = GraphML(file)

		result = simulate_onlineML(G)




