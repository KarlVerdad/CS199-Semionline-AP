import os
import argparse
import random
import numpy as np
from colorama import Fore
from datetime import datetime
from modules.GraphAP import GraphAP
from modules.GraphML import GraphML


SEED = [637534]		# Fallback seed
RESULTS_FILE = "../preliminary_results.txt"		# Relative path
VALID_EXT = ('.txt')		# Valid input file extensions

EPSILON_OPTIONS = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
K_OPTIONS = [10, 30, 50]
DELTA_OPTIONS = [0, 0.25, 0.5, 0.75, 1]
# DELTA_OPTIONS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]		# 0 => no unknowns, 1 => all unknown (δ - proportion of adversarial)
# DELTA_OPTIONS = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]


#region =====OnlineML=====

def simulate_onlineML(G: GraphML, seed):
	print(f"=== n: {G.n}, seed: {seed} ===")
	competitive_ratio_results = []

	for e in EPSILON_OPTIONS:
		for k in K_OPTIONS:
			np.random.seed(seed)

			predicted_graph = G.generate_perturbed_graph(0, e, k)
			predicted_matching = GraphML.get_optimal_matching(predicted_graph)
			predicted_sum = G.get_projected_matching_sum(predicted_matching)
			rmsd = G.calculate_rmsd(predicted_graph)

			# Consolidate Results
			empirical_competitive_ratio = predicted_sum / G.karp_sum
			data = (e, k, rmsd, empirical_competitive_ratio)
			competitive_ratio_results.append(data)

			# Display results
			print(f"ε: {e:.2f} | k: {k} | rmsd: {rmsd:.2f}")
			print(predicted_sum, "/", G.karp_sum)
			print(empirical_competitive_ratio)

	# Display summarized results
	print(f"===Summary===")
	summarized_results = [(round(e, 2), k, round(r, 2), round(c, 3)) for e, k, r, c in competitive_ratio_results]
	print("ε\tk\trmsd\tEmpirical C. Ratio")
	for e, k, r, c in summarized_results:
		print(f"{e}\t{k}\t{r}\t{c}")

	return competitive_ratio_results

#endregion

#region =====Semionline=====

## Performs semi-online matching on a graph
## Input: GraphAP class 'graphAP', proportion of unknown 'delta'
## Output: one-way matching dictionary
def semionline(graphAP: GraphAP, delta):
	matching = {}
	lookup = graphAP.generate_lookup_table(delta)

	# Pre-emptively marks all the nodes in lookup to reserve them
	for v, u in lookup.items():
		graphAP.set_matched(u, v)

	# Matching
	for v in range(graphAP.n, 2 * graphAP.n):
		if v in lookup:
			# Matching already exists
			u = lookup[v]
			matching[v] = u
		else:
			# Randomized Greedy Algorithm
			u = graphAP.get_closest(v)
			matching[v] = u
			graphAP.set_matched(u, v)

	return matching


## Base function for semionline matching [SEEDED]
## Input: absolute path to input 'file_path'
## Output: Dictionary of {delta: empirical c. ratio}
def simulate_semionline(G: GraphAP, seed):
	print(f"=== n: {G.n}, seed: {seed} ===")
	competitive_ratio_results = []

	for delta in DELTA_OPTIONS:
		np.random.seed(seed)
		G.flush()
		semionline_matching = semionline(G, delta)
		semionline_sum = G.get_projected_matching_sum(semionline_matching)

		# Consolidate results
		is_valid = G.is_matched_completely()
		if not is_valid:
			print(f"{Fore.RED}Error: Graph was not completely matched{Fore.WHITE}") 
		empirical_competitive_ratio = semionline_sum / G.karp_sum
		data = (delta, empirical_competitive_ratio)
		competitive_ratio_results.append(data)

		# Display results
		valid_text = f"{Fore.GREEN}(Valid){Fore.WHITE}" if is_valid \
		 	else f"{Fore.RED}(INVALID){Fore.WHITE}"

		print(f"Delta: {delta:.2f} {valid_text}")
		print(semionline_sum, "/", G.karp_sum)
		print(empirical_competitive_ratio)

	# Display summarized results
	print(f"===Summary===")
	# summarized_results = {d: round(c, 3) for d, c in competitive_ratio_results.items()}
	summarized_results = [(d, round(c, 3)) for d, c in competitive_ratio_results]
	print("Delta\tEmpirical C. Ratio")
	for d, c in summarized_results:
		print(f"{d}\t{c}")

	return competitive_ratio_results
	
#endregion

#region =====SemionlineML=====

def simulate_semionlineML(G: GraphML, seed):
	print(f"=== n: {G.n}, seed: {seed} ===")
	competitive_ratio_results = []

	for d in DELTA_OPTIONS:
		for e in EPSILON_OPTIONS:
			for k in K_OPTIONS:
				np.random.seed(seed)

				predicted_graph = G.generate_perturbed_graph(d, e, k)
				
				predicted_matching = GraphML.get_optimal_matching(predicted_graph)
				predicted_sum = G.get_projected_matching_sum(predicted_matching)
				rmsd = G.calculate_rmsd(predicted_graph)

				# Consolidate Results
				empirical_competitive_ratio = predicted_sum / G.karp_sum
				data = (d, e, k, rmsd, empirical_competitive_ratio)
				competitive_ratio_results.append(data)

				# Display results
				print(f"δ: {d:.2f} | ε: {e:.2f} | k: {k} | rmsd: {rmsd:.2f}")
				print(predicted_sum, "/", G.karp_sum)
				print(empirical_competitive_ratio)

	# Display summarized results
	print(f"===Summary===")
	summarized_results = [(round(d, 2), round(e, 2), k, round(r, 2), round(c, 3)) for d, e, k, r, c in competitive_ratio_results]
	print("δ\tε\tk\trmsd\tEmpirical C. Ratio")
	for d, e, k, r, c in summarized_results:
		print(f"{d}\t{e}\t{k}\t{r}\t{c}")

	return competitive_ratio_results

#endregion

#region Results Storing

## Converts a relative (to this file) path to an absolute path
## Input: directory containing file 'rel_dir', raw 'file_name'
## Output: absolute path to a single file
def rel2abs_path(rel_dir, file_name):
	dir = os.path.dirname(__file__)
	rel_path = os.path.join(dir, rel_dir, file_name)
	return os.path.abspath(rel_path)


## Appends results in the RESULTS_FILE
## Result must be a tuple of alphanumeric strings
def store_result(file_path, result, seed):
	# Stored data: File name, date, seed, n, results
	with open(file_path, "r") as f1:
		n = int(f1.readline())
	file_name = os.path.basename(file_path)
	time = datetime.now().strftime("%d %B %Y, %H:%M:%S")
	header = f"> {file_name} | {time} | Seed={seed} | n={n}\n"

	with open(rel2abs_path('.', RESULTS_FILE), "a") as f2:
		# Stores header
		f2.write(header)
		
		# Stores results line by line
		for i in range(len(result)):
			entry = "\t\t".join(str(data) for data in result[i])
			f2.write(f"{entry}\n")

#endregion

if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("algorithm", choices=["onlineML", "semionline", "semionlineML"],
			help="Type of Assignment Problem to simulate")
	parser.add_argument("path", 
			help="Directory/File to use as input")
	parser.add_argument("-S", "--save", action='store_true',
            help="Toggle to append the result(s) in the results file")

	seed_group = parser.add_mutually_exclusive_group()
	seed_group.add_argument("-s", "--seeds", type=int, nargs="+",
            help="Explicit seeds to use for randomization")
	seed_group.add_argument("-r", "--random", type=int,
			help="Count of non-explicit random seeds to use")

	args = parser.parse_args()

	# Process arguments
	seeds = []
	if args.random:
		for i in range(args.random):
			seeds.append(random.randint(0, 2 ** 32 - 1))	
	else:
		seeds = args.seeds if args.seeds else SEED

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
		# Create GraphAP
		print(f"=== File: {os.path.basename(file)} ===")

		if args.algorithm == "semionline":
			G = GraphAP(file)
			for seed in seeds:
				result = simulate_semionline(G, seed)
				print("")

				# Stores results
				if args.save:
					store_result(file, result, seed)
		else:
			G = GraphML(file)
			for seed in seeds:
				if args.algorithm == "onlineML":
					result = simulate_onlineML(G, seed)
				elif args.algorithm == "semionlineML":
					result = simulate_semionlineML(G, seed)
				print("")

				# Stores results
				if args.save:
					store_result(file, result, seed)

	if args.save:
			print(f"{Fore.GREEN}Results saved in {rel2abs_path('.', RESULTS_FILE)}{Fore.WHITE}")
	