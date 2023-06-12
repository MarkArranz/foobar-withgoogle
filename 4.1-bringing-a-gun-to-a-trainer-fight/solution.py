from itertools import product
from math import atan2


def solution(dimensions, your_position, trainer_position, distance):
    radius_squared = distance * distance
    dy = trainer_position[1] - your_position[1]
    dx = trainer_position[0] - your_position[0]

    if dx*dx + dy*dy > radius_squared:
        return 0
    
    prev_targets = set([atan2(dy, dx)])

    # Find how many mirrored rooms up and right you can reach
    rooms_up = distance // dimensions[1] + 1
    rooms_out = distance // dimensions[0] + 1

    # Find all self hit angles in the room.
    dys = [-your_position[1], 0, dimensions[1] - your_position[1]]
    dxs = [-your_position[0], 0, dimensions[0] - your_position[0]]
    thetas_self = {atan2(dy, dx):dx * dx + dy * dy
                   for dx,dy in product(dxs, dys)
                   if not (dx == 0 and dy == 0)}

    # Get all mirrored positions for the trainer and yourself.
    target_refs = getReflections(dimensions, trainer_position, rooms_up, rooms_out)
    your_refs = getReflections(dimensions, your_position, rooms_up, rooms_out)

    # Filter out your reflections that cannot be shot.
    for x,y in your_refs:
        dy = y - your_position[1]
        dx = x - your_position[0]
        theta_ref = atan2(dy,dx)
        delta_ref_sq = dx * dx + dy * dy

        if (delta_ref_sq <= radius_squared
            and (theta_ref not in thetas_self
                 or thetas_self[theta_ref] > delta_ref_sq)
         ):
            thetas_self[theta_ref] = delta_ref_sq

    # Find all targets that can be shot.
    for target in target_refs:
        dx = target[0] - your_position[0]
        dy = target[1] - your_position[1]
        theta_t = atan2(dy,dx)
        delta_t_sq = dx * dx + dy * dy

        if (delta_t_sq <= radius_squared 
            and theta_t not in prev_targets
            and (theta_t not in thetas_self
                or delta_t_sq < thetas_self[theta_t])
        ):
            prev_targets.add(theta_t)
    
    return len(prev_targets)


# Calculates mirrored positions.
def getReflections(dimensions, position, rooms_up, rooms_out):
    y_refs = (position[1], dimensions[1] - position[1])
    x_refs = (position[0], dimensions[0] - position[0])
    [x_offset, y_offset] = position
    refs_up = []
    refs_out = []

    y_toggle = True
    x_toggle = True

    for _ in range(rooms_up):
        y_offset += y_refs[y_toggle] * 2
        refs_up.append((position[0], y_offset))
        y_toggle = not y_toggle
    
    for _ in range(rooms_out):
        x_offset += x_refs[x_toggle] * 2
        refs_out.append((x_offset, position[1]))
        x_toggle = not x_toggle

    refs_up_and_out = [(out[0],up[1]) for out in refs_out for up in refs_up]
    reflections = [position] + refs_up + refs_out + refs_up_and_out
    reflections += [(-x,y) for x,y in reflections]
    reflections += [(x,-y) for x,y in reflections]

    return reflections

