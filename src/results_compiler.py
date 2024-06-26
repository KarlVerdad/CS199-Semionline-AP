###
# Averages results with the same n in prelimenary_results.txt to compiled_results.txt
# NOTE: Make sure not to try to compile data with incompatible algorithms or data sets
###

import os
from colorama import Fore


PRELIMS_FILE = "../preliminary_results.txt"		# Relative path
RESULTS_FILE = "../compiled_results.txt"		# Relative path


## Storage container for results
class Result:
	def __init__(self, header):
		# Prepare header information
		header_list = header.split("|")
		header_list[0] = header_list[0][1:]
		header_list = [s.strip() for s in header_list]

		# Extract info from header
		self.file = header_list[0]
		# self.date_created = datetime.strptime(header_list[1], "%d %B %Y, %H:%M:%S")	# No need to store date
		self.seeds = [int(header_list[2].split("=")[1])]
		self.n = int(header_list[3].split("=")[1])
		
		# Initialize results list
		self.data = []


	def __str__(self):
		return f"{self.file} | n={self.n} | Seeds={self.seeds}"

	__repr__ = __str__


	## Inserts data to data dictionary
	def insert_data(self, data_list):
		self.data.append([float(d) for d in data_list])

		
	def combine_data(self, index, new_value):
		count = len(self.seeds)
		total = self.data[index][-1] * count
		self.data[index][-1] = (total + new_value) / (count + 1)


	## Combines the data of another Results class by averaging them
	def combine(self, new_result):
		for i in range(len(new_result.data)):
			new_value = new_result.data[i][-1]
			self.combine_data(i, new_value)
		self.seeds.append(new_result.seeds[0])


## Reads and stores all the results in a single array
## Input: Relative path to results file 'results'
## Output: List of Result objects
def read_results(file_path):
	results = []
	in_chunk = False	# Tracks if reading results from a single file 

	with open(rel2abs_path('.', file_path), "r") as f:
		for line in f:
			line = line.strip()
			if line[0] == ">":
				# New chunk detected
				if in_chunk:
					# Save current chunk
					results.append(R)
					in_chunk = False

				in_chunk = True
				R = Result(line)
			else:
				# Data detected
				data = line.split("\t\t")
				R.insert_data(data)
		else:
			# Save current chunk
			results.append(R)

	return results


## Reads through the results and combines the same file names with different seeds
## Input: List of Result objects 'results'
## Output: Processed list of Result objects
def combine_results(results):
	unique_indices = {}		# Stores indices of unique file names

	for i in range(len(results)):
		r_curr: Result = results[i]
		if not r_curr.file in unique_indices:
			# Current i is unique (so far)
			unique_indices[r_curr.file] = i
			continue

		r_base: Result = results[unique_indices[r_curr.file]]
		if r_curr.seeds[0] in r_base.seeds:
			# Marks current i as a copy
			results[i] = None
			continue

		# Combine's the current i with base
		r_base.combine(r_curr)
		results[i] = None

	# Removes processed items (None type) in the list
	return [r for r in results if r != None]


## Appends Result data in the RESULTS_FILE
def store_result(result: Result):
	header = f"> {result.file} | n={result.n} | Count={len(result.seeds)} | Seeds={result.seeds}\n"

	with open(rel2abs_path('.', RESULTS_FILE), "a") as f:
		# Stores header
		f.write(header)
		
		# Stores results line by line
		for i in range(len(result.data)):
			entry = "\t\t".join(str(d) for d in result.data[i])
			f.write(f"{entry}\n")


## Converts a relative (to this file) path to an absolute path
## Input: directory containing file 'rel_dir', raw 'file_name'
## Output: absolute path to a single file
def rel2abs_path(rel_dir, file_name):
	dir = os.path.dirname(__file__)
	rel_path = os.path.join(dir, rel_dir, file_name)
	return os.path.abspath(rel_path)


if __name__ == "__main__":
	# Compiles results
	prelims = read_results(PRELIMS_FILE)
	results = combine_results(prelims)

	# Store results in file
	out_path = rel2abs_path('.', RESULTS_FILE) 
	open(out_path, "w").close()
	for r in results:
		store_result(r)

	print(f"{Fore.GREEN}Results saved in {out_path}{Fore.WHITE}")