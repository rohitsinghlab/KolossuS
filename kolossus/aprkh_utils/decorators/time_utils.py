
import time 
from functools import wraps


def main():
    @delay(0.3, 0.0)
    def foo(tsleep):
        time.sleep(tsleep)
        print("hello")

    for _ in range(int(3)):
        foo(0.2)


def delay(limit=1.0, time_delay=1.0):

    def decorator(func):
        # initializing to limit will ensure no delay on the first call
        state = {'prev_call': limit}

        @wraps(func)
        def wrapper(*args, **kwargs):

            # get current time 
            now = time.time()
            prev_call = state['prev_call']
            if abs(now - prev_call) < limit:
                time.sleep(time_delay)

            result = func(*args, **kwargs)

            state['prev_call'] = time.time()

            return result

        return wrapper

    return decorator


def fn_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        # run and time function
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"{func.__name__} took {elapsed_time:.3f} seconds to run.")
        return result
    return wrapper


if __name__ == '__main__': 
    main()
