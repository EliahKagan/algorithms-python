"""helpers - Some helper functions used in multiple modules."""

import functools


def optional_key_selector(function):
    """
    A decorator to allow an absent or None value for a keyword-only key
    argument (as used in functions like sort and min that do comparisons),
    replacing it with the identity function (facilitating "raw" comparison).
    """
    @functools.wraps(function)
    def wrapper(*args, key=None, **kwargs):
        if key is None:
            key = lambda x: x
        return function(*args, key=key, *kwargs)

    return wrapper


__all__ = [thing.__name__ for thing in (
    optional_key_selector,
)]
