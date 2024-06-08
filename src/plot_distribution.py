import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


def rel2abs_path(rel_dir, file_name):
	dir = os.path.dirname(__file__)
	rel_path = os.path.join(dir, rel_dir, file_name)
	return os.path.abspath(rel_path)


if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("path",
			help="Path to input")

	args = parser.parse_args()

	arr = []
	with open(rel2abs_path(".", args.path), "r") as f:
		f.readline()

		for line in f:
			arr = np.append(arr, list(map(float, line.strip().split(" "))))
	
	arr = [int(x) for x in arr]
	plt.hist(arr)
	plt.show()