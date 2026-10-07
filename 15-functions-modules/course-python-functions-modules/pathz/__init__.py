import functools
import os


def expand_tilde(path_func):
    """Decorator: expand ~ in the first positional argument before calling path_func."""
    @functools.wraps(path_func)
    def wrapped(first_component, *parts):
        return path_func(os.path.expanduser(first_component), *parts)
    return wrapped


def countit(fn):
    """Decorator: count and log every call to fn."""
    counter = 0

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal counter
        counter += 1
        result = fn(*args, **kwargs)
        print(f"count: {counter} {fn.__name__}")
        return result

    return wrapper


@expand_tilde
@countit
def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links."""
    try:
        os.stat(path)
    except (OSError, ValueError):
        return False
    return True


join = expand_tilde(countit(os.path.join))
abspath = expand_tilde(countit(os.path.abspath))
