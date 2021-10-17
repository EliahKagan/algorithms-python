#!/usr/bin/env python3

"""
sll - Singly Linked Lists

Implementations of "singly linked lists - creation and traversal" and
"singly linked lists - other common operations" sections in
https://github.com/EliahKagan/algorithms-suggestions/blob/master/algorithms-suggestions.md
(but adapted to Python).
"""

import helpers


class Node:
    """
    A singly linked list node.

    >>> Node('a parrot')
    Node('a parrot')
    >>> Node(1, Node(2, Node(3, Node(4, Node(5, Node(6))))))
    Node(1, Node(2, Node(3, Node(4, Node(5, Node(6))))))
    """

    __slots__ = ('value', 'next')

    def __init__(self, value, next=None):
        """Creates a singly linked list node."""
        self.value = value
        self.next = next

    def __repr__(self):
        """An eval-able text representation of this node (and its children)."""
        # FIXME: Do this iteratively to avoid stack overflow on long chains.
        if self.next is None:
            return f'Node({self.value!r})'
        return f'Node({self.value!r}, {self.next!r})'


def make_from(values):
    """
    Creates a singly linked list from an iterable of values.
    Returns the head node (or None if the sequence is empty).

    >>> make_from(())
    >>> make_from(('a parrot',))
    Node('a parrot')
    >>> make_from(range(5))
    Node(0, Node(1, Node(2, Node(3, Node(4)))))
    >>> make_from([10, 20, 30])
    Node(10, Node(20, Node(30)))
    >>> make_from([[10, 20, 30]])
    Node([10, 20, 30])
    """
    sentinel = Node(None)
    pre = sentinel

    for value in values:
        pre.next = Node(value)
        pre = pre.next

    return sentinel.next


def make(*values):
    """
    Creates a singly linked list from values passed as arguments.

    >>> make()
    >>> make('a parrot')
    Node('a parrot')
    >>> make(0, 1, 2, 3, 4)
    Node(0, Node(1, Node(2, Node(3, Node(4)))))
    >>> make(10, 20, 30)
    Node(10, Node(20, Node(30)))
    >>> make([10, 20, 30])
    Node([10, 20, 30])
    """
    return make_from(values)


def length(head):
    """
    Gets the length of a linked list when given the head node (or None for an
    empty list).

    >>> length(None)
    0
    >>> length(Node('ham'))
    1
    >>> length(Node('ham', Node('spam')))
    2
    >>> length(Node('ham', Node('spam', Node('eggs'))))
    3
    >>> length(Node('ham', Node('spam', Node('eggs', Node('speggs')))))
    4
    >>> length(make_from(range(100)))
    100
    """
    # This could be implemented in terms of the values function defined below,
    # but since it doesn't need the values, I implement it this way with the
    # intention that it will run faster.
    acc = 0
    while head:
        acc += 1
        head = head.next
    return acc


def get_values(head):
    """
    Yields the values of a linked list.

    >>> for x in get_values(make('foo', 'bar', 'baz', 'quux', 'foobar')):
    ...     print(x)
    foo
    bar
    baz
    quux
    foobar
    """
    while head:
        yield head.value
        head = head.next


def enumerate_values(head, start=0):
    """
    Enumerates the values in the linked list starting at head.

    >>> list(enumerate_values(make('foo', 'bar', 'baz', 'quux')))
    [(0, 'foo'), (1, 'bar'), (2, 'baz'), (3, 'quux')]
    >>> list(enumerate_values(make('foo', 'bar', 'baz', 'quux'), 1))
    [(1, 'foo'), (2, 'bar'), (3, 'baz'), (4, 'quux')]
    """
    return enumerate(get_values(head), start)


def as_list(head):
    """
    Converts a linked list to a Python list (which is a dynamic array).

    >>> as_list(None)
    []
    >>> as_list(make('foo', 'bar', 'baz', 'quux', 'foobar'))
    ['foo', 'bar', 'baz', 'quux', 'foobar']
    """
    return list(get_values(head))


def as_list_alt(head):
    """
    Converts a linked list to a Python list (which is a dynamic array).
    Alternative implementation.

    >>> as_list_alt(None)
    []
    >>> as_list_alt(make('foo', 'bar', 'baz', 'quux', 'foobar'))
    ['foo', 'bar', 'baz', 'quux', 'foobar']
    """
    ret = []
    while head:
        ret.append(head.value)
        head = head.next
    return ret


def find_index(head, value):
    """
    Finds the index of value in the list starting at head. Throws a ValueError
    if the value is not present (as list.index and str.index do).

    >>> h = Node('ham', Node('spam', Node('eggs', Node('speggs'))))
    >>> find_index(h, 'ham')
    0
    >>> find_index(h, 'spam')
    1
    >>> find_index(h, 'eggs')
    2
    >>> find_index(h, 'speggs')
    3
    >>> find_index(h, 'a parrot')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: 'a parrot' is not in linked list
    """
    for index, indexed_value in enumerate_values(head):
        if indexed_value == value:
            return index

    raise ValueError(f'{value!r} is not in linked list')


def find_index_alt(head, value):
    """
    Finds the index of value in the list starting at head. Throws a ValueError
    if the value is not present (as list.index and str.index do). Alternative
    implementation.

    >>> h = Node('ham', Node('spam', Node('eggs', Node('speggs'))))
    >>> find_index_alt(h, 'ham')
    0
    >>> find_index_alt(h, 'spam')
    1
    >>> find_index_alt(h, 'eggs')
    2
    >>> find_index_alt(h, 'speggs')
    3
    >>> find_index_alt(h, 'a parrot')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: 'a parrot' is not in linked list
    """
    index = 0
    while head:
        if head.value == value:
            return index
        index += 1
        head = head.next

    raise ValueError(f'{value!r} is not in linked list')


@helpers.optional_key_selector
def remove_min(head, *, key):
    """
    Removes the node with the minimum value (using a custom key selector if
    provided).

    If multiple values are minimal, the first is removed. If the list is empty,
    a ValueError is raised.

    >>> h = make('foo', 'bar', 'baz', 'quux', 'foobar')
    >>> h = remove_min(h)
    >>> h
    Node('foo', Node('baz', Node('quux', Node('foobar'))))
    >>> h = remove_min(h, key=len)
    >>> h
    Node('baz', Node('quux', Node('foobar')))
    >>> remove_min(Node('a parrot'))
    >>> remove_min(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: empty linked list has no minimum value
    """
    if head is None:
        raise ValueError('empty linked list has no minimum value')

    sentinel = Node(None, head)
    best = sentinel  # Identifies the head as having the min value so far.
    best_comparand = key(head.value)
    pre = head  # Because the first comparison will be made with head.next.

    while pre.next:
        comparand = key(pre.next.value)
        if comparand < best_comparand:
            best = pre
            best_comparand = comparand
        pre = pre.next

    best.next = best.next.next
    return sentinel.next


@helpers.optional_key_selector
def is_sorted(head, *, key):
    """
    Tells if a linked list is sorted. Uses the key selector if provided.

    >>> is_sorted(make_from(range(1000)))
    True
    >>> is_sorted(None)
    True
    >>> is_sorted(Node(1))
    True
    >>> is_sorted(Node(1, Node(2)))
    True
    >>> is_sorted(Node(2, Node(1)))
    False
    >>> is_sorted(Node(1, Node(2)), key=lambda x: -x)
    False
    >>> is_sorted(Node(2, Node(1)), key=lambda x: -x)
    True
    >>> is_sorted(make_from([42] * 1000))
    True
    >>> is_sorted(make(1, -1, 1, -1, 1, -1))
    False
    >>> is_sorted(make(1, -1, 1, -1, 1, -1), key=lambda x: -x)
    False
    >>> is_sorted(make(1, -1, 1, -1, 1, -1), key=abs)
    True
    >>> is_sorted(make('foo', 'bar', 'baz', 'quux', 'foobar'))
    False
    >>> is_sorted(make('foo', 'bar', 'baz', 'quux', 'foobar'), key=len)
    True
    >>> is_sorted(make('bar', 'baz', 'foo', 'foobar', 'quux'))
    True
    >>> is_sorted(make('bar', 'baz', 'foobar', 'foo', 'quux'))
    False
    """
    return helpers.is_sorted(get_values(head), key=key)


@helpers.optional_key_selector
def is_sorted_alt(head, *, key):
    """
    Tells if a linked list is sorted. Uses the key selector if provided.
    Alternative implementation.

    >>> is_sorted_alt(make_from(range(1000)))
    True
    >>> is_sorted_alt(None)
    True
    >>> is_sorted_alt(Node(1))
    True
    >>> is_sorted_alt(Node(1, Node(2)))
    True
    >>> is_sorted_alt(Node(2, Node(1)))
    False
    >>> is_sorted_alt(Node(1, Node(2)), key=lambda x: -x)
    False
    >>> is_sorted_alt(Node(2, Node(1)), key=lambda x: -x)
    True
    >>> is_sorted_alt(make_from([42] * 1000))
    True
    >>> is_sorted_alt(make(1, -1, 1, -1, 1, -1))
    False
    >>> is_sorted_alt(make(1, -1, 1, -1, 1, -1), key=lambda x: -x)
    False
    >>> is_sorted_alt(make(1, -1, 1, -1, 1, -1), key=abs)
    True
    >>> is_sorted_alt(make('foo', 'bar', 'baz', 'quux', 'foobar'))
    False
    >>> is_sorted_alt(make('foo', 'bar', 'baz', 'quux', 'foobar'), key=len)
    True
    >>> is_sorted_alt(make('bar', 'baz', 'foo', 'foobar', 'quux'))
    True
    >>> is_sorted_alt(make('bar', 'baz', 'foobar', 'foo', 'quux'))
    False
    """
    if head is None:
        return True

    pre = key(head.value)
    while head.next:
        head = head.next
        cur = key(head.value)
        if cur < pre:
            return False
        pre = cur

    return True


__all__ = [thing.__name__ for thing in (
    Node,
    make_from,
    make,
    length,
    get_values,
    enumerate_values,
    as_list,
    as_list_alt,
    find_index,
    find_index_alt,
    remove_min,
    is_sorted,
    is_sorted_alt,
)]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
