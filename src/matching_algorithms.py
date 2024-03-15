import networkx as nx
import numpy as np
import graph_operations as go
import data_generate as dg
from networkx.algorithms import bipartite
from scipy import sparse

def symmetric_diff(M1, M2):
    A = {M1[i] - int(len(M1) / 2) for i in range(int(len(M1) / 2))}
    B = {M2[i] - int(len(M2) / 2) for i in range(int(len(M2) / 2))}
    return A ^ B

def khuller(A):
    n = A.shape[0]
    lst = []
    B1 = sparse.csr_matrix(A[:1,:])
    G1 = bipartite.from_biadjacency_matrix(B1)
    M1 = bipartite.minimum_weight_full_matching(G1)
    lst.append((0, M1[0] - 1, int(A[0][M1[0] - 1])))

    for i in range(2, n + 1):
        B2 = sparse.csr_matrix(A[:i,:])
        G2 = bipartite.from_biadjacency_matrix(B2)
        M2 = bipartite.minimum_weight_full_matching(G2)
        col = list(symmetric_diff(M1, M2))[0]
        lst.append((i - 1, col, int(A[i - 1][col])))
        M1 = M2

    return lst
