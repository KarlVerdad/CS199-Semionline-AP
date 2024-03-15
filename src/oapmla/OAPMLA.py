import networkx as nx
import numpy as np
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import graph_operations as go
import run, math
import data_generate as dg


def algorithm_1(A, A_prime):
    # This is the ML Model substitute, feel free to modify
    # the inputs dg.perturb_choice(array, epsilon, k)
    A_prime, _ = algorithm_2(A, 0.3, 10)

    # Offline computation part.
    # sum output will return the total cost
    # zeros will return the matching
    sol, zeros = dg.compute_from_numpy(A_prime)

    # projection
    # Will simply project the matching zeros to
    # original array arr
    # returns an array with non-zeros on matching edges
    M = np.multiply(A, zeros)
    # Getting the total
    sol = np.sum(M)

    return M, sum


# Similar to perturb_choice function,
# included here for formalization purposes.
def algorithm_2(A, epsilon, k, seed=0):
    np.random.seed(seed)
    A_prime = np.copy(A)
    max_val = np.amax(A_prime)
    err = math.floor(A_prime.shape[0] * A_prime.shape[0] * epsilon)
    vals = A_prime[np.array(A_prime, dtype=bool)]
    err_indices = np.random.choice(range(vals.shape[0]),
                                   int(err),
                                   replace=False)
    for i in err_indices:
        if ((vals[i] + k) > max_val):
            vals[i] = int(math.floor(vals[i] - k))
            # print((vals[i] + (err*max_val)))
        elif ((vals[i] - k) < 0):
            vals[i] = int(math.floor(vals[i] + k))
            # print(vals[i])
        else:
            if (np.random.rand() > 0.5):
                vals[i] = int(math.floor(vals[i] + k))
            else:
                vals[i] = int(math.floor(vals[i] - k))
    A_prime[np.array(A_prime, dtype=bool)] = vals

    rmsd = np.sqrt(np.mean((A - A_prime)**2))
    return A_prime, rmsd