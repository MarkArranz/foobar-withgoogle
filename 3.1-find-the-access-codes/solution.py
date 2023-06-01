from itertools import combinations


def solution(l):
    """Counts the number of 'lucky triples' in a list.

    A "lucky triple" tuple of (a, b, c) where a, b, c are elements in list `l`,
    have the following properties:
      1. a divides b, that is, b % a == 0
      2. b divides c, that is, c % b == 0
      3. The indicies (i, j, k) of the tuple (a, b, c) meet the requirement:
           i < j < k.
    
    From this we can see that `b` is involved in two properties, first as
    a dividend to the divisor `a`, and second as the divisor to the dividend `c.`
    
    Therefore, for every combination of 2 elements in list `l`, if an element is
    a dividend during one valid calculation and a divisor during a different
    valid calculation, then those 2 combinations together make a "lucky triple."

    Args:
        l (List[int]): A list of positive integers.
    
    Returns:
        int: The count of 'lucky triples' in a list.

    Examples:
    >>> solution([1, 1, 1])
    1

    >>> solution([1, 2, 3, 4, 5, 6])
    3

    >>> solution([1, 1, 1, 1, 1])
    10 

    >>> solution([2, 3, 5, 7, 11])
    0

    >>> solution([1, 1])
    0
    """

    # Keep track of the number of times an element appears as a valid dividend.
    dividends = [0] * len(l)
    count = 0
    for i,j in combinations(range(0, len(l)), 2):
        # When an element a = l[i] divides element b = l[j] evenly...
        if l[j] % l[i] == 0:
            # ...increment the number of times element b = l[j] has been a valid dividend.
            dividends[j] += 1

            # Since element a = l[i] is a valid divisor, we can create lucky triples
            # for each time it has been a valid dividend.
            count += dividends[i]

    return count

import doctest
doctest.testmod()
