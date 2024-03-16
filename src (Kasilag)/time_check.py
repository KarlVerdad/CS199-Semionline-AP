import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from networkx.algorithms import bipartite
from scipy import sparse
from scipy.optimize import curve_fit

def create_graph_from_text(file_name):
    f = open(file_name)
    n = int(f.readline())

    A = np.array([]).astype(int)
    for line in f:
        A = np.append(A, list(map(int, line.strip().split(" "))))
    A = np.array(A).reshape(n,n)

    creation_time_s = time.perf_counter()
    G = nx.Graph()
    G.add_nodes_from(list(range(n)), bipartite=0)
    G.add_nodes_from(list(range(n,n*2)), bipartite=1)
    for i in range(n):
        G.add_weighted_edges_from([(i, x, A[i][x-n]) for x in range(n,n*2)])
    creation_time_e = time.perf_counter()
    creation_time = creation_time_e - creation_time_s
    
    # for line in bipartite.generate_edgelist(G):
    #     print(line)
    # print(minimum_weight_full_matching(G))
    
    # Visualization
    # l,r = nx.bipartite.sets(G)
    # pos = nx.bipartite_layout(G, l)
    # nx.draw(G, with_labels=True, pos=pos)
    # plt.show()

    f.close()

    return A, G, creation_time

def compute_sum_from_matching(A, M):
    n = A.shape[0]
    sum = 0

    for i in range(n):
        sum = sum + A[i][M[i] - n]

    return sum

def karp_time_function(x, A):
    # Assume that m = n
    y = A * (np.array(x) ** 2) * np.log10(x)
    return y

def main():
    n = 8
    attempts = 3
    creation_time = [[] for i in range(n)]
    matching_time = [[] for i in range(n)]

    if os.path.exists("../results/running_time_results.txt"):
        os.remove("../results/running_time_results.txt") 
    f = open("../results/running_time_results.txt", "x")
    
    for i in range(n): # there are 8 test data in Brunel
        for j in range(attempts): # repeated 3 times
            A, G, ctime = create_graph_from_text("../test/assign" + str((i + 1) * 100) + ".txt")
            creation_time[i].append(ctime)

            B = sparse.csr_matrix(A)
            G = bipartite.from_biadjacency_matrix(B)
            start = time.perf_counter()
            M = bipartite.minimum_weight_full_matching(G)
            end = time.perf_counter()
            matching_time[i].append(end - start)

            print("Input size: ", i + 1, ", Attempt: ", j + 1)
            print("Creation Time: ", ctime, ", Matching Time: ", end - start)

    f.write("Input size\tGraph Creation Time\tMatching Time\n")
    for i in range(n):
        for j in range(attempts):
            f.write("%i (Attempt %i)\t%s\t%s\n" % (((i + 1) * 100), (j + 1), 
                str(creation_time[i][j]), str(matching_time[i][j])))

    f.close()

    creation_time_ave = [np.average(creation_time[i]) for i in range(n)]
    matching_time_ave = [np.average(matching_time[i]) for i in range(n)]
    print("Graph Creation Average Time per Input Size: ", creation_time_ave)
    print("Bipartite Matching Average Time per Input Size: ", matching_time_ave)

    xlabel = [str((i + 1) * 100) for i in range(n)]
    fig, ax = plt.subplots()
    ax.bar(xlabel, creation_time_ave,
        label="Graph Creation")
    ax.bar(xlabel, matching_time_ave, 
        bottom=creation_time_ave, label="Bipartite Matching")
    ax.set_xlabel("Input size (n x n)")
    ax.set_ylabel("Time (in seconds)")
    ax.legend()
    plt.savefig("../results/running_time_results.png", dpi=600)
    plt.show()

    return 0

if __name__ == "__main__":
    main()
