from os import EX_IOERR
import random
import numpy as np
import math


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


def perturb_choice(arr_inp, epsilon, k, seed=0):
    np.random.seed(seed)
    arr = np.copy(arr_inp)
    max_val = np.amax(arr)
    err = math.floor(arr.shape[0] * arr.shape[0] * epsilon)
    vals = arr[np.array(arr, dtype=bool)]
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
    arr[np.array(arr, dtype=bool)] = vals

    rmsd = np.sqrt(np.mean((arr_inp - arr)**2))
    return arr, rmsd


def perturb_choice_partition(arr_inp, error, seed):
    np.random.seed(seed)
    arr = np.copy(arr_inp).flatten()
    err = int(arr.shape[0] * error)
    val_err = int(arr.sum() * error)
    err_indices = np.random.choice(range(arr.shape[0]),
                                   int(err),
                                   replace=False)
    if err != 0:
        x = val_err / err_indices.shape[0]
        for i in err_indices:
            arr[i] = arr[i] + x
    arr = np.reshape(arr, (arr_inp.shape[0], arr_inp.shape[1]))