import functools


def chain(*args):
    return functools.reduce(lambda f1, f2: f2(f1), reversed(args))

__all__ = ["chain"]
