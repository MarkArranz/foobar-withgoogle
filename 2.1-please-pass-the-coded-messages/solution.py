from functools import reduce
from itertools import combinations


def solution(l):
    """
    Finds the largest number that can be made from
    some or all of the digits and is divisible by 3.

    Uses the Divisibility Rule of 3 which states that any number whose sum
    of digits is divisible by 3 is also divisible by 3.

    Args:
        l (List[int]): A list of size 1 to 9 containing some digits (0 to 9).

    Returns:
        An integer value that meets the above criteria or
        0, if it is not possible to make such a number.

    Examples:

    >>> solution([3, 1, 4, 1])
    4311

    >>> solution([3, 1, 4, 1, 5, 9])
    94311
    """
    
    # Sorting from the largest digits to smallest digits will ensure we 
    # encounter the combo values from largest to smallest in our for loop.
    l.sort(reverse=True)

    if sum(l) % 3 == 0:
        return reduce(lambda acc, n: acc * 10 + n, l)

    digit_count = len(l)
    while digit_count > 0:
        seen = set()
        combos = combinations(l, digit_count)

        for c in combos:
            digit_sum = sum(c)
            if digit_sum not in seen:
                if digit_sum % 3 == 0:
                    return reduce(lambda acc, n: acc * 10 + n, c)
                else:
                    seen.add(digit_sum)

        digit_count -= 1

    return 0



import doctest

doctest.testmod()
