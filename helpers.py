#!/usr/bin/env python3

# Copyright (c) 2021, 2023 Eliah Kagan
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""Some helper functions used in multiple modules."""

__all__ = [
    'pairwise',
    'optional_key_selector',
    'is_sorted',
    'random_values',
]

import functools
import itertools
import random


def _pairwise(values):
    """
    Return length-2 windows into an iterable.

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


def equal(lhs, rhs):
    """
    Tell if two iterables represent the same sequence of values.

    The iterables can be arbitrarily long, so long as at least one of them is
    finite. They may be consumed. O(1) auxiliary space is used.
    """
    left_iterator = iter(lhs)
    right_iterator = iter(rhs)

    while True:
        try:
            left_value = next(left_iterator)
        except StopIteration:
            try:
                next(right_iterator)
            except StopIteration:
                return True
            return False

        try:
            right_value = next(right_iterator)
        except StopIteration:
            return False

        if left_value != right_value:
            return False


def _identity_function(arg):
    """Return the argument unchanged."""
    return arg


def optional_key_selector(function):
    """
    Decorate a function to allow an absent or None value for a "key" argument.

    This decorator allows an absent or None value for a keyword-only key
    argument, as used in functions like sort and min that do comparisons.

    Such an argument, when passed to the wrapper function, is replaced with the
    identity function (facilitating "raw" comparison).
    """
    @functools.wraps(function)
    def wrapper(*args, key=None, **kwargs):
        if key is None:
            key = _identity_function
        return function(*args, key=key, *kwargs)

    return wrapper


@optional_key_selector
def is_sorted(values, *, key):
    """
    Tell if an iterable is sorted. Use the key selector, if provided.

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


def random_values(count):
    """
    Generate the specified number of random values in a reasonable range.

    The range of values is the typical range of a 4-byte integer (i.e., the
    range of a 32-bit signed integer assuming two's complement).

    Returns a Python list of the generated values.
    """
    return [random.randint(-2**31, 2**31 - 1) for _ in range(count)]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
