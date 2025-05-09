#### Utilities for batching a computation. ####
#### taken from: https://github.com/aprkh/aprkh_utils/blob/main/decorators/batch_utils.py ####

from functools import wraps 
from functools import reduce 


# assumes that `func` is a function that operates on a list
class BatchComp():

    def __init__(self, block_size=10000):
        self.block_size = block_size

    def __call__(self, func):

        @wraps(func)
        def inner(data, *args, **kwargs):
            nobs = len(data)
            lo = 0
            niter = (nobs // self.block_size) + (0 if nobs % self.block_size == 0 else 1)
            results = [None for _ in range(niter)]
            ct = 0
            while lo < nobs:
                hi = min(lo + self.block_size, nobs)
                print(f"computing results for observations {lo+1} through {hi} out of {nobs}...", end=' ')            
                results[ct] = func(data[lo:hi], *args, **kwargs)
                print("done!")
                lo = hi
                ct += 1
            return results

        return inner

    def set_block_size(self, n):
        assert isinstance(n, int)
        assert n > 1
        self.block_size = n


def reduce_dict(dict_list):
    return reduce(update_dict, dict_list)


def update_dict(d1, d2):
    d1.update(d2)
    return d1
    
