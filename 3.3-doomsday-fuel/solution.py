from fractions import Fraction, gcd
from functools import reduce


def solution(m):
    """Predicts the ore state of an ore sample based on a transition matrix.

    Args:
        m (List[List[int]]): The transition matrix.
    
    Returns:
        List[int]: The numerators for the probabilities for each terminal state,
                    then the denominator at the end of the list.
    
    Examples:
    >>> solution([
    ...     [0, 2, 1, 0, 0],
    ...     [0, 0, 0, 3, 4],
    ...     [0, 0, 0, 0, 0],
    ...     [0, 0, 0, 0, 0],
    ...     [0, 0, 0, 0, 0],
    ... ])
    [7, 6, 8, 21]

    >>> solution([
    ...     [0, 1, 0, 0, 0, 1],
    ...     [4, 0, 0, 3, 2, 0],
    ...     [0, 0, 0, 0, 0, 0],
    ...     [0, 0, 0, 0, 0, 0],
    ...     [0, 0, 0, 0, 0, 0],
    ...     [0, 0, 0, 0, 0, 0],
    ... ])
    [0, 3, 2, 9, 14]
    """
    num_states = len(m)
    
    if num_states == 0:
        return []
    
    if sum(m[0]) == 0:
        return [1] + [0 for row in m[1:] if sum(row) == 0] + [1]
    
    transient_states = {}
    absorbing_states = {}
    for i in range(num_states):
        if sum(m[i]) == 0:
            absorbing_states[i] = len(absorbing_states)
        else:
            transient_states[i] = len(transient_states)

    t = len(transient_states)
    r = len(absorbing_states)
    
    # A t-by-t matrix where Q[i][j] is probability of transitioning
    # from the "i"-th transient state to the "j"-th transient state.
    Q = [[0 for _ in range(t)] for _ in range(t)]

    # A t-by-r matrix where R[i][j] is the probabilities of transitioning
    # from the "i"-th transient state to the "j"-th absorbing state.
    R = [[0 for _ in range(r)] for _ in range(t)]

    for source in range(num_states):
        for destination in range(num_states):
            if source in absorbing_states:
                continue

            total = sum(m[source])
            prob = Fraction(m[source][destination], total)
            from_t = transient_states[source]

            if destination in transient_states:
                to_t = transient_states[destination]
                Q[from_t][to_t] = prob
            else:
                to_a = absorbing_states[destination]
                R[from_t][to_a] = prob


    # Calculate the fundamental matrix N = (I_t - Q)**(-1)
    N = calculate_fundamental_matrix(Q)
    
    # The probability of being absorbed in the absorbing state `j`
    # when starting from transient state `i` is given by the `(i, j)`-entry
    # of the matrix B = NR
    B = multiply_matrix(N, R)

    # Since the ore starts in state 0 and
    # the processing always ends in a stable state,
    # we only need the first row of B.
    end_probs = B[0]

    # Calculate the least common denominator for all probabilities in `end_probs`.
    lcd = reduce(lcm, [p.denominator for p in end_probs])

    # Prepare the result to be of the following form:
    # [ *numerators, least_common_denominator ]
    result = [lcd / s.denominator * s.numerator for s in end_probs]
    result.append(lcd)

    return result


def calculate_fundamental_matrix(Q):
    # Check if Q is a valid input matrix
    n = len(Q)
    if n and n != len(Q[0]):
        raise ValueError("Input matrix must be square")

    # Create an identity matrix with the same dimensions as Q
    I = [[int(i == j) for i in range(n)] for j in range(n)]

    # Calculate the fundamental matrix N = (I_q - Q) ** -1
    return invert_matrix([[I[i][j] - Q[i][j] for j in range(n)] for i in range(n)])


def invert_matrix(matrix):
    n = len(matrix)
    # Check if the matrix is square
    if n and n != len(matrix[0]):
        raise ValueError("Input matrix must be square")

    # Augment the matrix with the identity matrix of the same size
    augmented = [row + [int(i == j) for i in range(n)] for j, row in enumerate(matrix)]

    # Perform Gaussian elimination to transform the augmented matrix to row-echelon form
    for i in range(n):
        # Find the row with the maximum value in the current column
        max_row = max(range(i, n), key=lambda x: abs(augmented[x][i]))

        # Swap the rows to bring the maximum value to the current row
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

        # Scale the current row to make the pivot equal to 1
        pivot = augmented[i][i]
        augmented[i] = [element / pivot for element in augmented[i]]

        # Eliminate the values above and below the current pivot
        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = [element - factor * augmented[i][k] for k, element in enumerate(augmented[j])]

    # Extract the inverted matrix from the augmented matrix
    return [row[n:] for row in augmented]


def multiply_matrix(matrix_A, matrix_B):
    # Check if the dimensions are valid for matrix multiplication.
    if len(matrix_A) and len(matrix_A[0]) != len(matrix_B):
        raise ValueError('Incompatible matrix dimensions.')

    return [[sum(a*b for a,b in zip(A_row, B_col))
             for B_col in zip(*matrix_B)]
             for A_row in matrix_A]


def lcm(a, b):
    """Finds the least common multiple of two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The least common multiple.
    """
    return abs(a * b) // gcd(a, b)


def test_solution():
    # Test case 1: Empty matrix
    m1 = []
    result1 = solution(m1)
    expected1 = []
    assert result1 == expected1, "Expected %s, but got %s" % (expected1, result1)

    # Test case 2: 1x1 matrix (single terminal state)
    m2 = [[0]]
    result2 = solution(m2)
    expected2 = [1, 1]
    assert result2 == expected2, "Expected %s, but got %s" % (expected2, result2)

    # Test case 3: 2x2 matrix (initial state to terminal state)
    m3 = [[0, 1], [0, 0]]
    result3 = solution(m3)
    expected3 = [1, 1]
    assert result3 == expected3, "Expected %s, but got %s" % (expected3, result3)

    # Test case 4: 4x4 matrix (terminal states in the middle)
    m4 = [[0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 0]]
    result4 = solution(m4)
    expected4 = [1, 1, 2]
    assert result4 == expected4, "Expected %s, but got %s" % (expected4, result4)

    # Test case 5: Matrix with all terminal states
    m5 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    result5 = solution(m5)
    expected5 = [1, 0, 0, 1]
    assert result5 == expected5, "Expected %s, but got %s" % (expected5, result5)

    print("All test cases passed.")

test_solution()

import doctest
doctest.testmod()
