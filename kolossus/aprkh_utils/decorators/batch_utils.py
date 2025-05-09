#### Utilities for batching a computation. ####


# assumes that `func` is a function that operates on a list
def batch_comp_on_list(block_size=10000):

    def decorator(func):

        def inner(data, *args, **kwargs):
            nobs = len(data)
            lo = 0
            niter = (nobs // block_size) + (0 if nobs % block_size == 0 else 1)
            results = [None for _ in range(niter)]
            ct = 0
            while lo < nobs:
                hi = min(lo + block_size, nobs)
                print(f"computing results for observations {lo} through {hi-1}...", end=' ')
                results[ct] = func(data[lo:hi], *args, **kwargs)
                print("done!")
                lo = hi
                ct += 1
            return results

        return inner

    return decorator 

