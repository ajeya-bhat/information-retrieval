import time
from utils import colorize

def timer_decorator(fn):
    def wrapper(param):
        start_ns = time.time()
        res = fn(param)
        end_ns = time.time()

        print(
            colorize.blue("Time Taken to run %s : %.4f"%(fn.__name__, end_ns-start_ns))
            )
        return res
    return wrapper