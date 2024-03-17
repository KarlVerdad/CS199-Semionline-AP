import random
from Classes.GraphAP import GraphAP
from colorama import Fore

random.seed(153123)

# Relative path in the eyes of GraphAP
#TODO: Add these as constants in GraphAP OR just use absolute paths 
TEST_FILE = "../../test/assign200.txt"	 
# 0 => no unknowns, 1 => all unknown
DELTA_OPTIONS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]


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


## Prototype function for semionline matchihng
## Input: relative path to input 'rel_path'
def simulate_semionline(rel_path):
	G = GraphAP(rel_path)

	# Offline matching (Karp)
	karp_matching = G.get_offline_matching()
	karp_sum = G.get_matching_sum(karp_matching)

	# Semi-online matching
	competitive_ratio_results = {}

	for delta in DELTA_OPTIONS:
		semionline_matching = semionline(G, delta)
		semionline_sum = G.get_matching_sum(semionline_matching)

		# Consolidate results
		is_valid = G.is_matched_completely()
		if not is_valid:
			print("Error: Graph was not completely matched")  #TODO: Make this a warning
		empirical_competitive_ratio = semionline_sum / karp_sum
		competitive_ratio_results[delta] = empirical_competitive_ratio

		# Display results
		valid_text = f"{Fore.GREEN}(Valid){Fore.WHITE}" if is_valid \
		 	else f"{Fore.RED}(INVALID){Fore.WHITE}"

		print(f"Delta: {'%.1f' % delta} {valid_text}")
		print(semionline_sum, "/", karp_sum)
		print(empirical_competitive_ratio)

	# Display summarized results
	print("==Summary==")
	print({d: float(f"{'%.4f' % c}") for d, c in competitive_ratio_results.items()})
	

if __name__ == "__main__":
	result = simulate_semionline(TEST_FILE)