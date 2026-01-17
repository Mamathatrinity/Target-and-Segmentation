import time
import functools

def retry_on_exception(max_retries=3, delay=1, exceptions=(Exception,)):
    """
    Decorator to retry a function on exception up to max_retries times.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
