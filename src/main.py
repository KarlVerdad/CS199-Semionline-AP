import random
from Classes.GraphAP import GraphAP


random.seed(10)

# Relative path in the eyes of GraphAP
#TODO: Add these as constants in GraphAP OR just use absolute paths 
TEST_FILE = "../../test/assign200.txt"	 
# 0 => no unknowns, 1 => all unknown
DELTA_OPTIONS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

## Prototype function for semionline matchihng
## Input: relative path to input 'rel_path'
def semionline(rel_path):
	G = GraphAP(rel_path)

	# Offline matching (Karp)
	karp_matching = G.get_offline_matching()
	karp_sum = G.get_matching_sum(karp_matching)

	# Semi-online matching
	lookup = G.generate_lookup_table(0.1)
	semionline_matching = {}

	# Pre-emptively matches all the nodes in lookup to reserve them
	for v, u in lookup.items():
		G.set_matched(u, v)

	# Proper semi-online matching
	for v in range(G.n, 2 * G.n):
		if v in lookup:
			# Matching already exists
			u = lookup[v]
			semionline_matching[v] = u
		else:
			# Randomized Greedy Algorithm
			u = G.get_closest(v)
			semionline_matching[v] = u
			G.set_matched(u, v)

	semionline_sum = G.get_matching_sum(semionline_matching)

	print("Completely matched:", G.is_matched_completely())
	print(semionline_sum, "/", karp_sum)
	print(semionline_sum / karp_sum)



if __name__ == "__main__":
	result = semionline(TEST_FILE)