
from functools import wraps 
from functools import reduce 


class DISCARD_COMPONENTS():

    def __init__(self, len_t, result_is_list, discard_set=None):
        self.discard_set = set() if not discard_set else(set(discard_set))
        self.result_is_list = result_is_list
        self.len_t = len_t

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if self.result_is_list:
                out = [self.remove_comps(x) for x in result]
            else:
                out = self.remove_comps(result)

            return out
        
        return wrapper

    def add_discard_index(self, *args):
        for i in args:
            if i < 0:
                i += self.len_t
            self.discard_set.add(i)

    def remove_comps(self, t):
        return tuple(x for i, x in enumerate(t) if i not in self.discard_set)
