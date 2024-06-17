###
# Generates a dataset in R2 Euclidean space
###

import math
import argparse
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore

MAX_RADIUS = 50


## Generates a list of uniformly distributed set of points inside a circle
def generate_points(max_radius, count):
	angle = np.random.uniform(0, 2 * np.pi, count)
	radius = (np.random.uniform(size=count) ** 0.5) * max_radius

	x = radius * np.cos(angle)
	y = radius * np.sin(angle)

	return (x, y)


## Get distance between 2 (x, y)-points
def get_distance(pointA, pointB):
		x_dist = abs(pointA[0] - pointB[0])
		y_dist = abs(pointA[1] - pointB[1])

		return math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2))


if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("n", type=int,
			help="Number of nodes in a partition")
	parser.add_argument("path",
			help="Path to store edges")

	args = parser.parse_args()
	
	# Generates 2 sets of points
	pointsU = generate_points(MAX_RADIUS, args.n)
	pointsV = generate_points(MAX_RADIUS, args.n)

	# Visualize data
	plt.scatter(pointsU[0], pointsU[1], s=5, c="r")
	plt.scatter(pointsV[0], pointsV[1], s=5, c="b")
	plt.show()

	# Calculate distances and save to file
	with open(args.path, "w") as f:
		f.write(f"{args.n}\n")

		for i in range(len(pointsU[0])):
			u = (pointsU[0][i], pointsU[1][i])
			weights = []

			for j in range(len(pointsV[0])):
				v = (pointsV[0][j], pointsV[1][j])
				w = get_distance(u, v)
				weights.append(round(w, 2))
			
			# Saves weights to file
			line = " ".join(map(str, weights))
			f.write(f"{line}\n")

	print(f"{Fore.GREEN}Results saved in {args.path}{Fore.WHITE}")

