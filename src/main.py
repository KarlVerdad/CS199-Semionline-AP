import os
import argparse
import random
from modules.GraphAP import GraphAP
from colorama import Fore
from datetime import datetime


SEED = 637534		# Fallback seed
RESULTS_FILE = "../preliminary_results.txt"		# Relative path
VALID_EXT = ('.txt', '.mama')		# Valid input file extensions
DELTA_OPTIONS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]		# 0 => no unknowns, 1 => all unknown


## Performs semi-online matching on a graph
## Input: GraphAP class 'graphAP', proportion of unknown 'delta'
## Output: one-way matching dictionary
def semionline(graphAP: GraphAP, delta):
	matching = {}
	graphAP.flush()
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
def simulate_semionline(file_path, seed):
	# Preliminaries
	file_name = os.path.basename(file_path)
	print(f"===File: {file_name}===")
	G = GraphAP(file_path)

	# Offline matching (Karp)
	karp_matching = G.get_offline_matching()
	karp_sum = G.get_matching_sum(karp_matching)

	# Semi-online matching
	competitive_ratio_results = {}

	for delta in DELTA_OPTIONS:
		random.seed(seed)
		semionline_matching = semionline(G, delta)
		semionline_sum = G.get_matching_sum(semionline_matching)

		# Consolidate results
		is_valid = G.is_matched_completely()
		if not is_valid:
			print(f"{Fore.RED}Error: Graph was not completely matched{Fore.WHITE}") 
		empirical_competitive_ratio = semionline_sum / karp_sum
		competitive_ratio_results[delta] = empirical_competitive_ratio

		# Display results
		valid_text = f"{Fore.GREEN}(Valid){Fore.WHITE}" if is_valid \
		 	else f"{Fore.RED}(INVALID){Fore.WHITE}"

		print(f"Delta: {delta:.2f} {valid_text}")
		print(semionline_sum, "/", karp_sum)
		print(empirical_competitive_ratio)

	# Display summarized results
	print(f"===Summary: {file_name}===")
	summarized_results = {d: round(c, 3) for d, c in competitive_ratio_results.items()}
	print("Delta\tEmpirical C. Ratio")
	for d, c in summarized_results.items():
		print(f"{d}\t{c}")

	return competitive_ratio_results
	

## Converts a relative (to this file) path to an absolute path
## Input: directory containing file 'rel_dir', raw 'file_name'
## Output: absolute path to a single file
def rel2abs_path(rel_dir, file_name):
	dir = os.path.dirname(__file__)
	rel_path = os.path.join(dir, rel_dir, file_name)
	return os.path.abspath(rel_path)


## Appends results in the RESULTS_FILE
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
		for d, c in result.items():
			entry = f"{d}\t\t{c}\n"
			f2.write(entry)


if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("path", help="Directory/File to use as input")
	parser.add_argument("-S", "--save", action='store_true',
            help="Toggle to append the result(s) in the results file")
	parser.add_argument("-s", "--seed", type=int,
            help="Seed to use for randomization")

	args = parser.parse_args()

	# Process arguments
	seed = args.seed if args.seed else SEED

	# Different behaviour based on if the path is a directory or file
	path = os.path.abspath(args.path)
	if os.path.isfile(path):
		# Path argument is a file
		result = simulate_semionline(path, seed)

		# Stores results
		if args.save:
			store_result(path, result, seed)

	elif os.path.isdir(path):
		# Path argument is a directory
		for file in sorted(os.listdir(path)):
			if file.endswith(VALID_EXT):
				file_path = os.path.join(path, file)
				result = simulate_semionline(file_path, seed)
				print("")

				# Store results
				if args.save:
					store_result(file_path, result, seed)

	else:
		raise Exception(f"{Fore.RED}Invalid path argument!{Fore.WHITE}")

	if args.save:
			print(f"Results saved in {rel2abs_path('.', RESULTS_FILE)}")
	