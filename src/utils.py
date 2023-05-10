import inspect
import time


def timeit(func: callable) -> callable:
    """
    Decorator that can be applied to any function to measure the execution time of that function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The resulting decorator function, which includes elapsed time measure to the console.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        caller_module = inspect.getframeinfo(inspect.stack()[1][0]).filename.split("/")
        print(
            f"{func.__name__} in {caller_module[-1]} elapsed time: {elapsed_time:.2f} seconds"
        )

        return result

    return wrapper
