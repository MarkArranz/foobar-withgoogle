def solution(start, length):
    """Generate security checksum.

    Args:
        start (int): The ID of the first worker to be checked.
        length (int): The length of the line before automatic review occurs.

    Returns:
        int: The security checksum.
    
    Examples:
    >>> solution(0, 3)
    2

    >>> solution(17, 4)
    14
    """
    checksum = 0
    # Holds the ID value for the last guard in line that will be checked.
    offset = length-1
    while offset >= 0:
        # Calculate the checksum for the consecutive IDs.
        checksum ^= xorBetween(start, start+offset)
        
        # Set start to be the value of the first ID for the next iteration.
        start += length
        # Check one less worker for the next iteration.
        offset -= 1

    return checksum


def consecutiveXor(n):
    """Calculates the XOR of consecutive numbers between 1 and `n` inclusive in comstant time.

    Args:
        n (int): The number to XOR up to and including. 

    Returns:
        int: The value if you XOR-ed all values from 1 up to and including `n`.
    """
    mod = n % 4
    if (mod == 0):
        return n
    elif (mod == 1):
        return 1
    elif (mod == 2):
        return n + 1
    else: # mod == 3
        return 0


def xorBetween(start, stop):
    """Calculates the XOR of consecutive numbers between `start` and `stop` inclusive in constant time.

    Args:
        start (int): The beginning number in a consecutive range.
        stop (int): The last number to XOR in a consecutive range.

    Returns:
        int: The value of XOR-ing consecutive numbers from `start` up to and including `stop`.
    """
    if start == 0:
        return consecutiveXor(stop)
    else:
        return consecutiveXor(start-1) ^ consecutiveXor(stop)


import doctest
doctest.testmod()
