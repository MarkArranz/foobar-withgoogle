from collections import deque
from itertools import product
from math import atan2


def solution(dimensions, your_position, trainer_position, distance):
    # Find how many mirrored rooms up and right you can reach
    rooms_up = distance // dimensions[1] + 1
    rooms_out = distance // dimensions[0] + 1

    # Find all self hit angles in the room.
    dys = [-your_position[1], 0, dimensions[1] - your_position[1]]
    dxs = [-your_position[0], 0, dimensions[0] - your_position[0]]
    thetas_self = {atan2(dy, dx):dx*dx+dy*dy
                   for dx,dy in product(dxs, dys)
                   if not (dx == 0 and dy == 0)}

    # Calculate reflection positions of you and trainer.
    trainer_y_refs = (trainer_position[1], dimensions[1] - trainer_position[1])
    trainer_x_refs = (trainer_position[0], dimensions[0] - trainer_position[0])
    [trainer_x_offset, trainer_y_offset] = trainer_position
    trainer_refs_up = []
    trainer_refs_out = []

    your_y_refs = (your_position[1], dimensions[1] - your_position[1])
    your_x_refs = (your_position[0], dimensions[0] - your_position[0])
    [your_x_offset, your_y_offset] = your_position
    your_refs_up = []
    your_refs_out = []

    y_toggle = True
    x_toggle = True

    for _ in range(rooms_up):
        new_trainer_ref = (trainer_position[0], 2*trainer_y_refs[y_toggle]+trainer_y_offset)
        trainer_y_offset = new_trainer_ref[1]
        trainer_refs_up.append(new_trainer_ref)

        new_your_ref = (your_position[0], 2*your_y_refs[y_toggle]+your_y_offset)
        your_y_offset = new_your_ref[1]
        your_refs_up.append(new_your_ref)

        y_toggle = not y_toggle
    
    for _ in range(rooms_out):
        new_trainer_ref = (2*trainer_x_refs[x_toggle]+trainer_x_offset, trainer_position[1])
        trainer_x_offset = new_trainer_ref[0]
        trainer_refs_out.append(new_trainer_ref)

        new_your_ref = (2*your_x_refs[x_toggle]+your_x_offset, your_position[1])
        your_x_offset = new_your_ref[0]
        your_refs_out.append(new_your_ref)

        x_toggle = not x_toggle

    trainer_refs_up_and_out = [(out[0],up[1]) for out in trainer_refs_out for up in trainer_refs_up]
    targets = [trainer_position] + trainer_refs_up + trainer_refs_out + trainer_refs_up_and_out
    targets += [(-x,y) for x,y in targets]
    targets += [(x,-y) for x,y in targets]

    your_refs_up_and_out = [(out[0],up[1]) for out in your_refs_out for up in your_refs_up]
    your_refs = your_refs_up + your_refs_out + your_refs_up_and_out
    your_refs += [(-x,y) for x,y in your_refs]
    your_refs += [(x,-y) for x,y in your_refs]

    for x,y in your_refs:
        dy = y-your_position[1]
        dx = x-your_position[0]
        theta_ref = atan2(dy,dx)
        delta_ref_sq = dx*dx+dy*dy

        if (theta_ref not in thetas_self
            or thetas_self[theta_ref] > delta_ref_sq):
            thetas_self[theta_ref] = delta_ref_sq


    r2 = distance*distance
    count = 0
    prev_theta_t = set()
    for target in targets:
        dx = target[0] - your_position[0]
        dy = target[1] - your_position[1]
        theta_t = atan2(dy,dx)
        delta_t_sq = dx*dx + dy*dy

        if (delta_t_sq <= r2 
            and theta_t not in prev_theta_t
            and (theta_t not in thetas_self
                or delta_t_sq < thetas_self[theta_t])
        ):
            prev_theta_t.add(theta_t)
            count += 1
    
    return count


        

if __name__ == '__main__':
    assert solution([3, 2], [1, 1], [2, 1], 4) == 7, solution([3, 2], [1, 1], [2, 1], 4)
    assert solution([2, 5], [1, 2], [1, 4], 11) == 27
    assert solution([23, 10], [6, 4], [3, 2], 23) == 8
    assert solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
    assert solution([10, 10], [4, 4], [3, 3], 5000) == 739323
    assert solution([3, 2], [1, 1], [2, 1], 7) == 19
    assert solution([2, 3], [1, 1], [1, 2], 4) == 7
    assert solution([3, 4], [1, 2], [2, 1], 7) == 10
    assert solution([4, 4], [2, 2], [3, 1], 6) == 7
    assert solution([300, 275], [150, 150], [180, 100], 500) == 9