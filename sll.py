#!/usr/bin/env python3

"""
sll - Singly Linked Lists

Implementations of "singly linked lists - creation and traversal" and
"singly linked lists - other common operations" sections in
https://github.com/EliahKagan/algorithms-suggestions/blob/master/algorithms-suggestions.md
(but adapted to Python).
"""

import itertools

import helpers
import warmup


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
    # This could be implemented in terms of the get_values function defined
    # below, but since it doesn't need the values, I implement it this way with
    # the intention that it will run faster.
    acc = 0
    while head:
        acc += 1
        head = head.next
    return acc


def get_nodes(head):
    """
    Yields the nodes of a linked list.

    >>> for x in get_nodes(make('foo', 'bar', 'baz', 'quux', 'foobar')):
    ...     print(x.value)
    foo
    bar
    baz
    quux
    foobar
    """
    while head:
        yield head
        head = head.next


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
    # This could be implemented in terms of the get_nodes function implemented
    # above, but I've done it separately with the intention that it will run
    # slightly faster.
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


def put(head):
    """
    Prints all values in the linked list on a line, separated by commas and
    whitespace, ended with a period.

    >>> h = make(10, 20, 30, 40, 50, 60, 70)
    >>> put(h)
    10, 20, 30, 40, 50, 60, 70.
    >>> put(Node('foo'))
    foo.
    >>> put(None)
    .
    """
    warmup.put(get_values(head))


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


def advance(head, distance):
    """
    Returns the node the specified distance away from head. Returns None if
    there is no such node.

    >>> h = make('first', 'second', 'third', 'fourth', 'fifth')
    >>> advance(h, -1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: can't advance a negative distance in a singly linked list
    >>> put(advance(h, 0))
    first, second, third, fourth, fifth.
    >>> put(advance(h, 1))
    second, third, fourth, fifth.
    >>> put(advance(h, 2))
    third, fourth, fifth.
    >>> put(advance(h, 3))
    fourth, fifth.
    >>> put(advance(h, 4))
    fifth.
    >>> put(advance(h, 5))
    .
    >>> put(advance(h, 6))
    .
    >>> put(advance(h, 7))
    .
    >>> put(advance(h, 1000))
    .
    """
    if distance < 0:
        raise ValueError(
            "can't advance a negative distance in a singly linked list")

    for _ in range(distance):
        if head is None:
            return None
        head = head.next

    return head


def split(head):
    """
    Splits a linked list into halves. Returns the head of the second half.
    If the number of nodes is odd, the first list has one more node.

    >>> a1 = make(10, 20, 30, 40, 50)
    >>> a2 = split(a1)
    >>> put(a1)
    10, 20, 30.
    >>> put(a2)
    40, 50.
    >>> b1 = make(10, 20, 30, 40, 50, 60)
    >>> b2 = split(b1)
    >>> put(b1)
    10, 20, 30.
    >>> put(b2)
    40, 50, 60.
    >>> c1 = Node('a parrot')
    >>> c2 = split(c1)
    >>> put(c1)
    a parrot.
    >>> put(c2)
    .
    >>> d1 = None
    >>> d2 = split(d1)
    >>> put(d1)
    .
    >>> put(d2)
    .
    >>> e1 = make('foo', 'bar')
    >>> e2 = split(e1)
    >>> put(e1)
    foo.
    >>> put(e2)
    bar.
    >>> f1 = make('jam', 'yam', 'kegs')
    >>> f2 = split(f1)
    >>> put(f1)
    jam, yam.
    >>> put(f2)
    kegs.
    >>> g1 = make('Mary', 'Larry', 'Bari', 'Terry')
    >>> g2 = split(g1)
    >>> put(g1)
    Mary, Larry.
    >>> put(g2)
    Bari, Terry.
    """
    if head is None:
        return None

    fast = head.next
    while fast and fast.next:
        head = head.next
        fast = fast.next.next

    mid = head.next
    head.next = None
    return mid


def split_alt(head):
    """
    Splits a linked list into halves. Returns the head of the second half.
    If the number of nodes is odd, the first list has one more node.
    Alternative implementation.

    >>> a1 = make(10, 20, 30, 40, 50)
    >>> a2 = split_alt(a1)
    >>> put(a1)
    10, 20, 30.
    >>> put(a2)
    40, 50.
    >>> b1 = make(10, 20, 30, 40, 50, 60)
    >>> b2 = split_alt(b1)
    >>> put(b1)
    10, 20, 30.
    >>> put(b2)
    40, 50, 60.
    >>> c1 = Node('a parrot')
    >>> c2 = split_alt(c1)
    >>> put(c1)
    a parrot.
    >>> put(c2)
    .
    >>> d1 = None
    >>> d2 = split_alt(d1)
    >>> put(d1)
    .
    >>> put(d2)
    .
    >>> e1 = make('foo', 'bar')
    >>> e2 = split_alt(e1)
    >>> put(e1)
    foo.
    >>> put(e2)
    bar.
    >>> f1 = make('jam', 'yam', 'kegs')
    >>> f2 = split_alt(f1)
    >>> put(f1)
    jam, yam.
    >>> put(f2)
    kegs.
    >>> g1 = make('Mary', 'Larry', 'Bari', 'Terry')
    >>> g2 = split_alt(g1)
    >>> put(g1)
    Mary, Larry.
    >>> put(g2)
    Bari, Terry.
    """
    total_length = length(head)
    if total_length < 2:
        return None

    head = advance(head, (total_length - 1) // 2)
    mid = head.next
    head.next = None
    return mid


def last(head):
    """
    Finds the last node of a linked list. Returns None if there are no nodes.

    >>> last(None)
    >>> last(Node(10))
    Node(10)
    >>> last(make(10, 20))
    Node(20)
    >>> last(make(10, 20, 30))
    Node(30)
    >>> last(make_from(range(100)))
    Node(99)
    """
    if head is None:
        return None

    while head.next:
        head = head.next

    return head


def concat(first, second):
    """
    Concatenates two linked lists. Returns the head of the concatenated list.

    >>> put(concat(None, None))
    .
    >>> put(concat(None, Node('spam')))
    spam.
    >>> put(concat(Node('ham'), None))
    ham.
    >>> put(concat(Node('ham'), Node('spam')))
    ham, spam.
    >>> put(concat(make(10), make(20, 30)))
    10, 20, 30.
    >>> put(concat(make(10, 20), make(30, 40)))
    10, 20, 30, 40.
    >>> put(concat(make_from(range(10)), make_from(range(15, 20))))
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19.
    """
    sentinel = Node(None, first)
    last(sentinel).next = second
    return sentinel.next


def _connect(nodes):
    """
    Connects nodes from an iterable in the order in which they were passed.
    Assumes nodes are distinct. Returns the head node, or None if the iterable
    was empty.

    This is a helper function for timsort.

    >>> _connect([])
    >>> _connect([Node(10)])
    Node(10)
    >>> _connect([Node(10), Node(20)])
    Node(10, Node(20))
    >>> put(_connect([Node(10), Node(20), Node(30)]))
    10, 20, 30.
    >>> put(_connect(Node(x) for x in range(10)))
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9.
    """
    sentinel = Node(None)
    chain = itertools.chain((sentinel,), nodes, (None,))
    for left, right in helpers.pairwise(chain):
        left.next = right
    return sentinel.next


@helpers.optional_key_selector
def timsort(head, *, key):
    """
    Copies the nodes of a linked list to a Python list, sorts it, and
    reconnects the nodes.

    >>> put(timsort(None))
    .
    >>> put(timsort(Node(10)))
    10.
    >>> put(timsort(make(20, 10)))
    10, 20.
    >>> put(timsort(make(10, 20)))
    10, 20.
    >>> put(timsort(make(1, 7, 4, 9, 2, 6, 1, 8, 3, -5)))
    -5, 1, 1, 2, 3, 4, 6, 7, 8, 9.
    """
    return _connect(sorted(get_nodes(head), key=lambda node: key(node.value)))


@helpers.optional_key_selector
def timsort_alt(head, *, key):
    """
    Copies the nodes of a linked list to a Python list, sorts it, and
    reconnects the nodes.

    >>> put(timsort_alt(None))
    .
    >>> put(timsort_alt(Node(10)))
    10.
    >>> put(timsort_alt(make(20, 10)))
    10, 20.
    >>> put(timsort_alt(make(10, 20)))
    10, 20.
    >>> put(timsort_alt(make(1, 7, 4, 9, 2, 6, 1, 8, 3, -5)))
    -5, 1, 1, 2, 3, 4, 6, 7, 8, 9.
    """
    if head is None:
        return None

    values = []
    while head:
        values.append(head)
        head = head.next

    values.sort(key=lambda node: key(node.value))

    for left, right in helpers.pairwise(values):
        left.next = right
    values[-1].next = None

    return values[0]


__all__ = [thing.__name__ for thing in (
    Node,
    make_from,
    make,
    length,
    get_nodes,
    get_values,
    enumerate_values,
    as_list,
    as_list_alt,
    find_index,
    find_index_alt,
    remove_min,
    is_sorted,
    is_sorted_alt,
    advance,
    split,
    split_alt,
    last,
    concat,
)]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
