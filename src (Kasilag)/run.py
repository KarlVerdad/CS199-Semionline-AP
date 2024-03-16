# 10. Run the algorithm on the set of all test data. 
import numpy as np
import graph_operations as go


# GETS ALL PERMUTATIONS OF THE INPUT SEQUENCE
def permute(arr, size, mm=0):
    if (mm == size):
        print(go.compute_from_numpy(arr))
        return
    else:
        for i in range(mm, size+1):
            arr[[mm, i]] = arr[[i, mm]]
            permute(arr, size, mm+1)
            arr[[mm, i]] = arr[[i, mm]]

def generate_choice_matrix(A, M):
    choice_graph = np.zeros([A.shape[0], A.shape[0]])
    for i in range(A.shape[0]):
        choice_graph[i][M[i]-A.shape[0]] = 1
    return choice_graph