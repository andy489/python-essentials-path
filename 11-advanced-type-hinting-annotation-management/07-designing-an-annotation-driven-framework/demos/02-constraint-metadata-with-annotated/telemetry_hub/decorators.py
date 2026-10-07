import functools
import sys
import time
from collections.abc import Callable


def retry[**P, R](times: int = 3) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"retry: {wrapper.__name__} attempt {attempt} failed",
                        file=sys.stderr,
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def instrument[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            print(
                f"instrument: {wrapper.__name__} took {elapsed_ms:.1f}ms",
                file=sys.stderr,
            )

    return wrapper
