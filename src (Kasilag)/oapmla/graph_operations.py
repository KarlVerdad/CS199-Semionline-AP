import networkx as nx
import numpy as np
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import data_generate as dg


# Generates a networkx graph from a text file
# Input: text file 'file_name'
# Output: numpy array 'A', graph 'G'
def create_graph_from_text(file_name):
    f = open(file_name)
    n = int(f.readline())

    A = np.array([]).astype(int)
    for line in f:
        A = np.append(A, list(map(int, line.strip().split(" "))))
    A = np.array(A).reshape(n, n)

    G = nx.Graph()
    G.add_nodes_from(list(range(n)), bipartite=0)
    G.add_nodes_from(list(range(n, n * 2)), bipartite=1)
    for i in range(n):
        G.add_weighted_edges_from([(i, x, A[i][x - n])
                                   for x in range(n, n * 2)])
    f.close()
    return A, G


# Generates a networkx file from a numpy array
# Input: numpy array 'array'
# Output: networkx graph 'G"
def create_graph_from_numpy(array):
    G = nx.Graph()
    n = array.shape[0]
    G.add_nodes_from(list(range(n)), bipartite=0)
    G.add_nodes_from(list(range(n, n * 2)), bipartite=1)
    for i in range(n):
        G.add_weighted_edges_from([(i, x, array[i][x - n])
                                   for x in range(n, n * 2)])

    return G


# Computes the optimal matching of a bipartite graph
# Input: numpy array 'array'
# Output: return of function compute_sum_from_matching
def compute_from_numpy(array):
    G = create_graph_from_numpy(array)
    M = bipartite.minimum_weight_full_matching(G)
    return compute_sum_from_matching(array, M)  # returns sum and zeros


# Computes the sum from the matching obtained
# Input: original array 'A', matching 'M'
# Output: sum of matching 'sum', zeros of A 'zeros'
def compute_sum_from_matching(A, M):
    n = A.shape[0]
    zeros = np.zeros([A.shape[0], A.shape[1]])
    sum = 0

    for i in range(n):
        sum = sum + A[i][M[i] - n]
        zeros[i][M[i] - n] = 1

    return sum, zeros


def run_projection(arr, epsilon, k):
    rmsd_arr = []
    pred_arr, rmsd = dg.perturb_choice(arr, epsilon, k)
    rmsd_arr.append(rmsd)
    sum, zeros = compute_from_numpy(pred_arr)
    sol = np.sum(np.multiply(arr, zeros))
    return sol, rmsd_arr


def iterate_for_increasing_n_graph(file_name, err_list, k):
    sol = []
    rmsd_list = []
    arr, graph = create_graph_from_text(file_name)
    optimal_offline = compute_from_numpy(arr)
    print("Optimal solution from Karp: ", optimal_offline[0])
    for i in err_list:
        sol_, rmsd = run_projection(arr, i, k)
        rmsd_list.append(rmsd)
        sol.append(np.mean(sol_) / optimal_offline[0])
    return sol, rmsd


def iterate_for_different_error(file_name_list, epsilon, k):
    sol = []
    rmsd_list = []
    for i in file_name_list:
        arr, graph = create_graph_from_text(i)
        optimal_offline = compute_from_numpy(arr)
        sol_, rmsd = run_projection(arr, epsilon, k)
        rmsd_list.append(rmsd)
        sol.append(np.mean(sol_) / optimal_offline[0])
    print("done")
    return sol, rmsd_list


def iterate_get_rmsd(file_name_list, epsilon_list, k_list):
    arr, graph, rmsd_list, sol_list = [], [], [], []
    for i in file_name_list:
        arr.append(create_graph_from_text(i)[0])
    for i in arr:
        opt = compute_from_numpy(i)[0]
        for j in epsilon_list:
            for k in k_list:
                sol, rmsd = run_projection(i, j, k)
                rmsd_list.append(rmsd)
                sol_list.append(sol / opt)
    return sol_list, rmsd_list
