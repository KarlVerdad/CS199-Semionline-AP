###
# Plots the distribution of datasets
# Additionally shows the quantitative descriptions of the dataset (i.e. mean, variance)
###

import argparse
import statistics as st
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore



if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("path",
			help="Path to input")

	args = parser.parse_args()

	arr = []
	with open(args.path, "r") as f:
		f.readline()

		for line in f:
			arr = np.append(arr, list(map(float, line.strip().split(" "))))
	
	arr = [int(x) for x in arr]
	print(f"Mean: {Fore.GREEN}{np.mean(arr)}{Fore.WHITE}")
	print(f"Median: {Fore.GREEN}{np.median(arr)}{Fore.WHITE}")
	print(f"Mode: {Fore.GREEN}{st.mode(arr)}{Fore.WHITE}")
	print(f"Variance: {Fore.GREEN}{np.var(arr)}{Fore.WHITE}")

	plt.hist(arr)
	plt.show()