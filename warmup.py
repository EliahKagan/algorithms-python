#!/usr/bin/env python3

"""
Implementations for warmup exercises in
https://github.com/EliahKagan/algorithms-suggestions/blob/master/algorithms-suggestions.md
(but adapted to Python).
"""

from timeit import timeit
from helpers import optional_key_selector


def put(values):
    """
    Prints values on a line, separated by commas, ended with a period.

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
    Sorts a list of values in place using Python's sort method for lists.

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
    Sorts a list of numbers in ascending order, but with all odds first.

    >>> a = [1, 7, 4, 9, 2, 6, 1, 8, 3, -5]
    >>> sort_with_odds_first(a)
    >>> a
    [-5, 1, 1, 3, 7, 9, 2, 4, 6, 8]
    """
    nums.sort(key=lambda num: (num % 2 == 0, num))


def find_index(values, value):
    """
    Does sequential search in values for key. Returns an index where the key
    appears, or None if the sequences of values doesn't contain the key.

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


@optional_key_selector
def insertion_sort(values, *, key):
    """
    Sorts values in place by insertion sort, using the key selector if given.

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
    Merges values[low:mid] and values[mid:high] back into values[:], using
    aux as auxiliary storage. Each range is assumed to be sorted relative to
    < with the specified key selector.

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


@optional_key_selector
def mergesort(values, *, key):
    """
    Sorts values in place by recursive top-down mergesort, using the key
    selector if given.

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


@optional_key_selector
def mergesort_bottomup(values, *, key):
    """
    Sorts values in place by iterative bottom-up mergesort, using the key
    selector if given.

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
    Benchmarks all three sorting algorithms implemented here, by sorting copies
    of values with each of them.
    """
    sorted_values = sorted(values)
    quantity = '1 value' if len(values) == 1 else f'{len(values)} values'

    for sorter in (insertion_sort, mergesort, mergesort_bottomup):
        # Pylint wrongly thinks hoisting the copy out of the loop would be OK.
        # pylint: disable=cell-var-from-loop
        # Pylint thinks key= is mandatory (it doesn't understand my decorator).
        # pylint: disable=missing-kwoa
        # FIXME: How about when @optional_key_selector uses @functools.wraps?
        copied_values = values[:]
        duration = timeit(lambda: sorter(copied_values), number=1)
        if copied_values != sorted_values:
            raise AssertionError('Sorting failed!')
        print(f'On {quantity}, {sorter.__name__} took {duration * 1000} ms.')


__all__ = [thing.__name__ for thing in (
    put,
    timsort,
    sort_with_odds_first,
    find_index,
    insertion_sort,
    mergesort,
    mergesort_bottomup,
    benchmark_sorts,
)]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
