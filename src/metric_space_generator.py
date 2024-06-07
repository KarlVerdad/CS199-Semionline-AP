## Generates the edges of a bipartite graph in a Euclidean metric space
## Metric space is a square with edges that have a length of METRIC_SPACE_LIMIT
import os
import math
import random
import argparse


METRIC_SPACE_LIMIT = 100

class Point:
	def __init__(self):
		self.x, self.y = Point.generate_coordinates()

	def __str__(self):
		return f"({self.x}, {self.y})"

	def __repr__(self):
		return self.__str__()
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def set_coordinates(self, x, y):
		self.x = x
		self.y = y

	## STATIC FUNCTION
	def generate_coordinates():
		x = random.randint(0, METRIC_SPACE_LIMIT)
		y = random.randint(0, METRIC_SPACE_LIMIT)
		return (x, y)

	def distance_to(self, point):
		x_dist = abs(point.x - self.x)
		y_dist = abs(point.y - self.y)

		return math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2))


def rel2abs_path(rel_dir, file_name):
	dir = os.path.dirname(__file__)
	rel_path = os.path.join(dir, rel_dir, file_name)
	return os.path.abspath(rel_path)


if __name__ == "__main__":
	# Parameters
	parser = argparse.ArgumentParser()

	parser.add_argument("n", type=int,
			help="Number of nodes in a partition")
	parser.add_argument("path",
			help="Relative path to store edges")

	args = parser.parse_args()

	# Generate points
	points = []

	for i in range(2 * args.n):
		p = Point()

		# Prevents duplicate points
		while True:
			for q in points:
				if p == q:
					x, y = Point.generate_coordinates()
					# print(f"{p} --> {(x, y)}")
					p.set_coordinates(x, y)
					continue
			break
	
		points.append(p)

	# Calculates distances and saves them to file
	pointsU = points[:args.n]
	pointsV = points[args.n:]

	with open(rel2abs_path(".", args.path), "w") as f:
		f.write(f"{args.n}\n")

		for u in pointsU:
			weights = []

			for v in pointsV:
				w = u.distance_to(v)
				weights.append(round(w, 2))
			
			# Saves weights to file
			line = " ".join(map(str, weights))
			f.write(f"{line}\n")
