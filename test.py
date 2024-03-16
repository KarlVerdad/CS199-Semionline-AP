import numpy as np
import networkx as nx
import math
from networkx.algorithms import bipartite

# Generate an upper triangular of 1s with shape (x,x)
def generate_matrixA(x):
	if (x <= 0):
		raise Exception(
			"You cannot create a matrix with zero or negative shape.")
	else:
		arr = np.ones([x, x])
		arr[np.tril_indices(arr.shape[0], -1)] = 2
	return arr


def get_error_choices(shape, err):
	error_indices = np.random.choice(range(shape), err, replace=True)
	print(type(error_indices))


def perturb_choice(arr_inp, epsilon, k, seed=0):
	np.random.seed(seed)		## OLD IMPLEMENTATION
	arr = np.copy(arr_inp)
	max_val = np.amax(arr)
	err = math.floor(arr.shape[0] * arr.shape[0] * epsilon)  # Number of indices to change
	print("err:", err)
	vals = arr[np.array(arr, dtype=bool)]	# Changes the array to a 1D array for easy modification
	print("vals:", vals )
	err_indices = np.random.choice(range(vals.shape[0]),
								   int(err),
								   replace=False)
	print("indices:", err_indices)
	for i in err_indices:
		if ((vals[i] + k) > max_val):
			vals[i] = int(math.floor(vals[i] - k))
			# print((vals[i] + (err*max_val)))
		elif ((vals[i] - k) < 0):	## Curiously, they used 0 instead of minimum value in the matrix
			vals[i] = int(math.floor(vals[i] + k))
			# print(vals[i])
		else:
			if (np.random.rand() > 0.5):
				vals[i] = int(math.floor(vals[i] + k))
			else:
				vals[i] = int(math.floor(vals[i] - k))
	arr[np.array(arr, dtype=bool)] = vals

	rmsd = np.sqrt(np.mean((arr_inp - arr)**2))
	return arr, rmsd



arr_inp = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

def perturb_choice_partition(arr_inp, error, seed):
	np.random.seed(seed)
	arr = np.copy(arr_inp).flatten()
	err = int(arr.shape[0] * error)
	val_err = int(arr.sum() * error)
	err_indices = np.random.choice(range(arr.shape[0]),
								   int(err),
								   replace=False)
	print(err_indices)
	if err != 0:
		x = val_err / err_indices.shape[0]
		print(x)
		for i in err_indices:
			arr[i] = arr[i] + x
	arr = np.reshape(arr, (arr_inp.shape[0], arr_inp.shape[1]))

	print(arr)


# Generates a networkx graph from a text file
# Input: text file 'file_name'
# Output: numpy array 'A', graph 'G'
def create_graph_from_text(file_name):
	count = 0
	f = open(file_name)
	n = int(f.readline())

	A = np.array([]).astype(int)
	for line in f:
		add = list(map(int, line.strip().split(" ")))
		# print(add)
		count += len(add)
		A = np.append(A, add)
	A = np.array(A).reshape(n, n)

	G = nx.Graph()
	G.add_nodes_from(list(range(n)), bipartite=0)			# Sets 'bipartite' attribute to 0 (LHS)
	# print("==Addition 1==")
	# print(list(range(n)))
	G.add_nodes_from(list(range(n, n * 2)), bipartite=1)	# Sets 'bipartite' attribute to 0 (LHS)
	# print("==Addition 2==")
	# print(list(range(n, n * 2)))

	for i in range(n):
		G.add_weighted_edges_from([(i, x, A[i][x - n])
								   for x in range(n, n * 2)])
	f.close()

	# print(f"Total Elements: {count}")
	return A, G



# Computes the sum from the matching obtained
# Input: original array 'A', matching 'M'
# Output: sum of matching 'sum', zeros of A 'zeros'
def compute_sum_from_matching(A, M):
	# print(A)
	# print(M)
	n = A.shape[0]
	zeros = np.zeros([A.shape[0], A.shape[1]])
	sum = 0

	for i in range(n):
		# print(i, "->", A[i][M[i] - n])
		sum = sum + A[i][M[i] - n]		# A contains node i's edge weights; M contains matched node offset by n
		zeros[i][M[i] - n] = 1			# Sets node i's matched node to 1

	return sum, zeros


def sample_assign100(fName):
	A, G = create_graph_from_text(fName)
	M = bipartite.minimum_weight_full_matching(G)
	sumVal = compute_sum_from_matching(A, M)
	return sumVal, A, M, G

sum, A, M, G = sample_assign100("test/assign200.txt")

### Check out A and G contents ###
print(A[0])
# print(A[1])
# print(A[2])


n = A.shape[0]

# Prints the edges of the first node of the LHS
LHS_edges = [G.edges[0, i + 200]["weight"] for i in range(n)]
print("==LHS==")
print(LHS_edges)

# RHS_edges = [G.edges[]]


######


# print(type(sum[0]))


# print(sum)
# print(len(sum[1]))


# total = 0
# for i in range(len(sum[1])):
# 	for j in range(len(sum[1][i])):
# 		if sum[1][i][j] != 0:
# 			total += sum[1][i][j]
# 	# print(sum[1][i])

# print(total)
# print(type(sum))

# print(M)
# print(type(M))
# print(G.edges[335, 5])


# =================

# arr, graph = create_graph_from_text("test/assign200.txt")


# print(arr)
# print(len(arr))
# print(len(arr[0]))
# print(type(arr))

# print(graph)
# print(type(graph))
# print(graph.nodes)
# print(graph.nodes[0]["bipartite"])

# print(graph.edges)
# print(graph.number_of_edges())
# print(graph.number_of_edges(0, 200))
# print(graph.edges.data())
# print(graph.edges[0, 200])
# print(graph.edges[199, 399]["weight"])

