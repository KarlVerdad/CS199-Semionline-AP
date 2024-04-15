import os
import argparse
import numpy as np
from colorama import Fore
from modules.GraphML import GraphML


VALID_EXT = ('.txt')		# Valid input file extensions


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


	# Testing
	for file in input_files:
		G = GraphML(file)
		predicted_graph = G.generate_perturbed_graph(0.5, 10)


