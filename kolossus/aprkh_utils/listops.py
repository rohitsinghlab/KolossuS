#### misc operations on lists 

import math 


def batch_list(A, n):
    """
    Splits the list A into batches of size n. 
    """
    nbatches = math.ceil(len(A) / n)
    out = [None for _ in range(nbatches)]
    for i, j in enumerate(range(0, len(A), n)):
        out[i] = A[j:j+n]
    return out


def order_cols(A, f, *args, reverse=False, **kwargs):
    """
    Orders columns of a 2D-array A according to functional f. 

    (Assumes A is a numpy array or something similar like a tensor).
    """
    keys = list(range(len(A[0])))
    keys_sorted = sorted(keys, key=lambda i: f(A[:, i], *args, **kwargs), reverse=reverse)
    return keys_sorted, A[:, keys_sorted]

