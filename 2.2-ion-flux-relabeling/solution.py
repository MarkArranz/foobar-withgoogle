def solution(h, q):
    """Finds the parent label for each converter listed in q, respectively.

    Args:
        h (int): The height of the perfect tree of converters.
        q (List[int]): A list of positive integers representing different
                       flux converters.

    Returns:
        List[int]: A list consisting of positive integers or -1.

    Examples:
    >>> solution(5, [19, 14, 28])
    [21, 15, 29]

    >>> solution(3, [7, 3, 5, 1])
    [-1, 7, 6, 3]
    """
    return [findParentLabel(c, h, c, h) for c in q]


def getRootLabel(h):
    """Calculates a flux chain's root label given the flux chain's height.

    Flux chains require perfect binary trees. A perfect binary tree of
    height `h` has `n` number of nodes by the formula:

        n = 2 ** (h + 1) - 1

    where `h` equals 0 represents a single node tree.

    Commander Lambda performed a post-order traversal of the tree of
    converters and labeled each converter with the order of that
    converter in the traversal, starting at 1.

    Therefore, the number of nodes in a flux chain of height `h - 1` also
    gives us the label for the root of a flux chain of the same height.

        2 ** ((h - 1) + 1 ) - 1
        => 2 ** h - 1

    Args:
        h (int): The height of a flux chain where h = 1 represents a single
                 node tree.

    Returns:
        int: The label for the root of the flux chain.
    """
    return 2**h - 1


def findParentLabel(
    current_label, current_height, original_label, original_height, isLeft=True
):
    """Finds the parent label for a given flux converter.

    Uses a binary search algorithm to locate a given flux converter in a
    flux converter tree and calculate the flux converter's parent's label.

    Args:
        current_label (int):
            The label of the current node.
        current_height (int):
            The current level in a tree.
        original_label (int):
            The original label of the node when the search first began.
        original_height (int):
            The original height of the tree when the search first began.
        isLeft (bool, optional):
            Is the current node a left child? Defaults to True.

    Returns:
        int: The label of the parent node.
    """
    root_label = getRootLabel(current_height)
    if current_label == root_label:
        if current_height == original_height:
            return -1
        elif isLeft:
            return root_label + original_label + 1
        else:
            return original_label + 1
    else:
        # Since Commander Lambda performed a post-order traversal of the tree
        # to label each converter, labels less than or equal to the midpoint
        # label are located in the left child, whereas labels greater than
        # the midpoint are located in the right child.
        mid = root_label // 2
        if current_label <= mid:
            return findParentLabel(
                current_label,
                current_height - 1,
                original_label,
                original_height,
                True,
            )
        else:
            return findParentLabel(
                current_label - mid,
                current_height - 1,
                original_label,
                original_height,
                False,
            )


import doctest

doctest.testmod()
