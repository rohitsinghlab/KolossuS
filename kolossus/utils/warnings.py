
import functools
from functools import wraps 

import sys 
import inspect

# FLAGS to be concerned about 
FLAGS = {274: ('print_warning_message_flag_274', 'check_testing')}


def main():
    foo(False) 
    foo(True)
    foo(False)


# decorators to wrap function 
def warn(flag, warn_condition=None):

    def decorator(func):
    
        @wraps(func)
        def wrapper(*args, **kwargs):
            wfn, cfn = FLAGS.get(flag, ('all_good', 'always_true'))
            warn_func = globals().get(wfn)
            cond_func = globals().get(cfn)

            # figure out whether or not we have to warn
            if cond_func(func, *args, **kwargs):
                # get function info 
                name = func.__name__
                file = inspect.getfile(func)
                line_num = inspect.getsourcelines(func)[1]
                warn_func(flag, name, file, line_num)
                
            result = func(*args, **kwargs)
            
            return result
        return wrapper

    return decorator


@warn(274)
def foo(testing):
    print('foo')


# printing warning messages 
def all_good(flag, name, file, line_num, *args, **kwargs):
    err("WARNING: INVALID FLAG CALLED:", flag)
    err(f"SEE FUNCTION {name} IN FILE {file}, LINE {line_num}")
    

# special decorator called here 
def print_warning_message_flag_274(flag, name, file, line_num):
    err("WARNING: FLAG 274: OBTAINING JUNK SEQUENCES", end='! ')
    err(f"SEE FUNCTION {name} IN FILE {file}, LINE {line_num}")


# condition checkers
def always_true(func, *args, **kwargs):
    return True


def check_testing(func, *args, **kwargs):
    arg_values = inspect.getcallargs(func, *args, **kwargs)
    if arg_values.get('testing') == True:
        return True
    return False
    

def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == '__main__': 
    main()
