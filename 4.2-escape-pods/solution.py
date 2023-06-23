import doctest


def solution(sources, sinks, capacity):
    """
    Calculates how many bunnies can safely make it to the escape pods at a
    time at peak using the the push-relabel maximum flow algorithm.

    Args:
        sources (List[int]):
            The starting room numbers of the groups of bunnies.
        sinks (List[int]):
            The room numbers of the escape pods.
        capacity (List[List[int]]):
            How many bunnies can git through at a time in each direction of
            every corridor in between.

    Returns:
        int: The total number of bunnies that can get through at each time step.

    Examples:
    >>> solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
    6
    >>> solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
    16
    """
    num_nodes = len(capacity)
    flow = [[0] * num_nodes for _ in range(num_nodes)]
    height = [0] * num_nodes
    excess_flow = [0] * num_nodes
    visited = [0] * num_nodes
    q = [i for i in range(num_nodes) if i not in sources and i not in sinks]

    def push(v, w):
        flow_to_push = min(excess_flow[v], capacity[v][w] - flow[v][w])
        flow[v][w] += flow_to_push
        flow[w][v] -= flow_to_push
        excess_flow[v] -= flow_to_push
        excess_flow[w] += flow_to_push

    def relabel(v):
        min_height = num_nodes
        for w in range(num_nodes):
            if capacity[v][w] - flow[v][w] > 0:
                min_height = min(min_height, height[w])
                height[v] = min_height + 1

    def discharge(v):
        while excess_flow[v] > 0:
            if visited[v] < num_nodes:
                w = visited[v]
                if capacity[v][w] - flow[v][w] > 0 and height[v] > height[w]:
                    push(v, w)
                else:
                    visited[v] += 1
            else:
                relabel(v)
                visited[v] = 0

    for s in sources:
        height[s] = num_nodes
        excess_flow[s] = float("inf")
        for w in range(num_nodes):
            push(s, w)

    i = 0
    while i < len(q):
        v = q[i]
        old_height = height[v]
        discharge(v)
        if height[v] > old_height:
            q.insert(0, q.pop(i))
            i = 0
        else:
            i += 1

    max_flow = sum([sum(flow[s]) for s in sources])

    return max_flow


doctest.testmod()
