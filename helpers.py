#!/usr/bin/env python3

"""helpers - Some helper functions used in multiple modules."""

import functools
import itertools


def _pairwise(values):
    """
    Returns length-2 windows into an iterable.

    On Python 3.10 and greater, itertools.pairwise exists and should be
    preferred.

    >>> list(pairwise(range(5)))
    [(0, 1), (1, 2), (2, 3), (3, 4)]
    >>> list(pairwise(range(1)))
    []
    """
    iterator = iter(values)
    try:
        pre = next(iterator)
    except StopIteration:
        return

    for cur in iterator:
        yield pre, cur
        pre = cur


try:
    pairwise = itertools.pairwise
except AttributeError:
    pairwise = _pairwise


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


@optional_key_selector
def is_sorted(values, *, key):
    """
    Tells if an iterable is sorted. Uses the key selector if provided.

    >>> is_sorted(range(1000))
    True
    >>> is_sorted(())
    True
    >>> is_sorted((1,))
    True
    >>> is_sorted((1, 2))
    True
    >>> is_sorted((2, 1))
    False
    >>> is_sorted((1, 2), key=lambda x: -x)
    False
    >>> is_sorted((2, 1), key=lambda x: -x)
    True
    >>> is_sorted([42] * 1000)
    True
    >>> is_sorted([1, -1, 1, -1, 1, -1])
    False
    >>> is_sorted([1, -1, 1, -1, 1, -1], key=lambda x: -x)
    False
    >>> is_sorted([1, -1, 1, -1, 1, -1], key=abs)
    True
    >>> is_sorted(['foo', 'bar', 'baz', 'quux', 'foobar'])
    False
    >>> is_sorted(['foo', 'bar', 'baz', 'quux', 'foobar'], key=len)
    True
    >>> is_sorted(['bar', 'baz', 'foo', 'foobar', 'quux'])
    True
    >>> is_sorted(['bar', 'baz', 'foobar', 'foo', 'quux'])
    False
    """
    return all(key(lhs) <= key(rhs) for lhs, rhs in pairwise(values))


__all__ = [thing.__name__ for thing in (
    pairwise,
    optional_key_selector,
    is_sorted,
)]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
