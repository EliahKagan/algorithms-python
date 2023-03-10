#!/usr/bin/env python

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

"""
Implementations for warmup exercises in
https://github.com/EliahKagan/algorithms-suggestions/blob/master/algorithms-suggestions.md
(but adapted to Python).
"""

__all__ = [
    'put',
    'timsort',
    'sort_with_odds_first',
    'find_index',
    'insertion_sort',
    'mergesort',
    'mergesort_bottomup',
    'benchmark_sorts',
]

import timeit

import helpers


def put(values):
    """
    Print a line of values.

    Values are separated by commas and whitespace. The line ends with a period.

    >>> a = [10, 20, 30, 40, 50, 60, 70]
    >>> put(a)
    10, 20, 30, 40, 50, 60, 70.
    >>> put(['foo'])
    foo.
    >>> put(())
    .
    """
    print(*values, sep=', ', end='.\n')


def timsort(values):
    """
    Sort a list of values in place using Python's sort method for lists.

    >>> a = [1, 7, 4, 9, 2, 6, 1, 8, 3, -5]
    >>> b = a[:]
    >>> timsort(a)
    >>> a == sorted(b)
    True
    >>> put(a)
    -5, 1, 1, 2, 3, 4, 6, 7, 8, 9.
    """
    values.sort()


def sort_with_odds_first(nums):
    """
    Sort a list of numbers in ascending order, but with all odds first.

    >>> a = [1, 7, 4, 9, 2, 6, 1, 8, 3, -5]
    >>> sort_with_odds_first(a)
    >>> a
    [-5, 1, 1, 3, 7, 9, 2, 4, 6, 8]
    """
    nums.sort(key=lambda num: (num % 2 == 0, num))


def find_index(values, value):
    """
    Do a sequential search in values for the given value.

    If value is present, its index is returned. Otherwise, None is returned.

    >>> a = [1, 7, 4, 9, 2, 6, 1, 8, 3, -5]
    >>> find_index(a, 3)
    8
    >>> find_index(a, 7)
    1
    >>> find_index(a, 5)
    >>>
    """
    try:
        return values.index(value)
    except ValueError:
        return None


@helpers.optional_key_selector
def insertion_sort(values, *, key):
    """
    Sort values in place by insertion sort, using the key selector if given.

    >>> a = [1, 7, 4, 9, 2, 6, 1, 8, 3, -5]
    >>> insertion_sort(a)
    >>> a
    [-5, 1, 1, 2, 3, 4, 6, 7, 8, 9]
    >>> insertion_sort(a, key=lambda x: -x)
    >>> a
    [9, 8, 7, 6, 4, 3, 2, 1, 1, -5]
    >>> insertion_sort(a, key=abs)
    >>> a
    [1, 1, 2, 3, 4, -5, 6, 7, 8, 9]
    """
    for right in range(1, len(values)):
        for left in range(right, 0, -1):
            if key(values[left - 1]) <= key(values[left]):
                break
            values[left - 1], values[left] = values[left], values[left - 1]


def _merge(values, low, mid, high, aux, key):
    """
    Merge consecutive slices, using the given auxiliary list.

    This merges values[low:mid] and values[mid:high] back into values[:], using
    aux as auxiliary storage. Each range is assumed to be sorted relative to <
    with the specified key selector.

    This is a helper function for mergesort and mergesort_bottomup.
    """
    assert not aux, 'The auxiliary storage is expected to start empty.'

    left = low
    right = mid

    while left < mid and right < high:
        if key(values[right]) < key(values[left]):
            aux.append(values[right])
            right += 1
        else:
            aux.append(values[left])
            left += 1

    aux.extend(values[left:mid])
    assert len(aux) == right - low, 'Wrong number of values copied.'
    values[low:right] = aux
    aux.clear()


@helpers.optional_key_selector
def mergesort(values, *, key):
    """
    Sort by recursive top-down mergesort.

    This sorts values by recursive top-down mergesort. If a key selector is
    supplied, it is used. The values list is modified.

    >>> a = [1, 7, 4, 9, 2, 6, 1, 8, 3, -5]
    >>> mergesort(a)
    >>> a
    [-5, 1, 1, 2, 3, 4, 6, 7, 8, 9]
    >>> mergesort(a, key=lambda x: -x)
    >>> a
    [9, 8, 7, 6, 4, 3, 2, 1, 1, -5]
    >>> mergesort(a, key=abs)
    >>> a
    [1, 1, 2, 3, 4, -5, 6, 7, 8, 9]
    """
    aux = []

    def mergesort_sublist(low, high):
        delta = high - low
        if delta < 2:
            return
        mid = low + delta // 2
        mergesort_sublist(low, mid)
        mergesort_sublist(mid, high)
        _merge(values, low, mid, high, aux, key)

    mergesort_sublist(0, len(values))


@helpers.optional_key_selector
def mergesort_bottomup(values, *, key):
    """
    Sort by iterative bottom-up mergesort.

    This sorts values by iterative bottom-up mergesort. If a key selector is
    supplied, it is used. The values list is modified.

    >>> a = [1, 7, 4, 9, 2, 6, 1, 8, 3, -5]
    >>> mergesort_bottomup(a)
    >>> a
    [-5, 1, 1, 2, 3, 4, 6, 7, 8, 9]
    >>> mergesort_bottomup(a, key=lambda x: -x)
    >>> a
    [9, 8, 7, 6, 4, 3, 2, 1, 1, -5]
    >>> mergesort_bottomup(a, key=abs)
    >>> a
    [1, 1, 2, 3, 4, -5, 6, 7, 8, 9]
    """
    aux = []

    delta = 1
    while delta < len(values):
        for low in range(0, len(values) - delta, delta * 2):
            mid = low + delta
            high = min(mid + delta, len(values))
            _merge(values, low, mid, high, aux, key)
        delta *= 2


def benchmark_sorts(values):
    """
    Benchmark all three sorting algorithms in the warning module.

    This runs and returns timings of all three sorting algorithms implemented
    in this module. It works by sorting separate copies of the values sequence
    with each of them.
    """
    sorted_values = sorted(values)
    quantity = '1 value' if len(values) == 1 else f'{len(values)} values'

    for sorter in (insertion_sort, mergesort, mergesort_bottomup):
        # Pylint wrongly thinks hoisting the copy out of the loop would be OK.
        # pylint: disable=cell-var-from-loop
        # Pylint doesn't understand decorators and thinks key= is mandatory.
        # pylint: disable=missing-kwoa
        copied_values = values[:]
        duration = timeit.timeit(lambda: sorter(copied_values), number=1)

        if copied_values != sorted_values:
            raise AssertionError(f'Sorting with {sorter.__name__} failed!')

        formatted_duration = f'{(duration * 1000):.0f} ms'
        print(f'On {quantity}, {sorter.__name__} took {formatted_duration}.')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
