import functools

def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                try:
                    new_args = args + (c if isinstance(c, tuple) else (c,))
                    f(*new_args)
                except Exception as e:
                    print (str(e),new_args)
                    raise

        return wrapper
    return decorator