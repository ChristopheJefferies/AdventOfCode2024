filename = "input13.txt"

import math


# Parse input
machines = []
machine = []
with open(filename) as file:
    for line in file:
        words = line.split()
        if not words:  # Blank line between machines
            machines.append(machine)
            machine = []
        else:
            machine.append(int(words[-2][2:-1]))
            machine.append(int(words[-1][2:]))
    machines.append(machine)  # No newline at end of file


# Quick and dumb approach for part 1
def min_cost_for_prize(machine: list[int]) -> int:
    """
    Input: a list of 6 ints representing button A, button B, and the target
    Output: The minimum cost of pressing buttons to reach the prize if it is
        possible with <= 100 presses of each button, or 0 if it is impossible.
    """

    Ax, Ay, Bx, By, Px, Py = machine

    # Find all solutions with at most 100 button presses each
    min_cost = math.inf
    for A_presses in range(101):
        if (Px < 0) or (Py < 0):
            break

        if Px % Bx == 0:  # x coord can be fixed with B presses from here
            B_presses = Px // Bx
            if By * B_presses == Py:  # y coord matches target, solution found
                min_cost = min(min_cost, (3 * A_presses) + B_presses)

        # Modify these in-place to track remaining movement needed
        Px -= Ax
        Py -= Ay

    if min_cost == math.inf:
        return 0
    return min_cost


total_cost = 0
for machine in machines:
    total_cost += min_cost_for_prize(machine)
print(total_cost)


# Smarter approach for part 2

"""
If the two button presses are non-parallel (as vectors in 2D):
    There's either a unique linear combination of the vectors that hits the target, or none
    Use the extended Euclidean alg to find a pair u, v such that u*Ax + v*Bx = g := gcd(Ax, Bx)
    Do a quick check of gcd's in both coordinates to eliminiate obviously-unreachable prizes
    Multiply them both by Px//g to get a particular solution u'*Ax + v'*Bx = Px
        All solutions are then given by adding multiples of (-Bx/g,Ax/g) to (u',v')
    Try adjusting solution to hit the Y coordinate. Compute u'*Ay + v'*By and the step -Bx*Ay/g + Ax*By/g
        Add multiples of the step (in the right direction) until we hit/pass the target, check for positivity, and return cost

If the two vectors are parallel:
    Can no longer assume there's a unique linear combination of the vectors that hits the target
    But the AOC creators seemed not to test us with these. Not complaining on a busy day :)
"""


def extended_gcd(a: int, b: int) -> tuple[int]:
    """
    Extended gcd algorithm, as described e.g. on Wikipedia.
    Outputs:
        gcd(a, b)
        Bezout coefficients u, v such that a*u + b*v = gcd(a, b)
    """

    if a == 0 or b == 0:
        return max(a, b), 1, 1

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    return old_r, old_s, old_t


def min_cost_for_prize2(machine: list[int]) -> tuple[int]:
    """
    Input: a list of 6 ints representing button A, button B, and the target
    Output: The minimum cost of pressing buttons to reach the prize if it is
        possible, or 0 if it is impossible.
    """

    Ax, Ay, Bx, By, Px, Py = machine

    # Check for vectors being parallel
    if Ay * Bx == By * Ax:
        raise AssertionError("AOC gave us nice inputs that never hit this :)")

    g, u, v = extended_gcd(Ax, Bx)

    # Quick Euclidean alg checks for obviously-unreachable prizes
    if Px % g != 0:
        return 0
    if Py % math.gcd(Ay, By) != 0:
        return 0

    # Hit a particular solution for the target in the x coordinate
    scale = Px // g
    u *= scale
    v *= scale

    # Check if another solution can hit the y coordinate
    current_y = u * Ay + v * By
    step = (-Bx // g) * Ay + (Ax // g) * By
    if (Py - current_y) % step != 0:
        return 0

    # Find the u and v which hit the target
    num_steps = (Py - current_y) // step
    u += num_steps * (-Bx // g)
    v += num_steps * (Ax // g)

    if (u < 0) or (v < 0):
        return 0

    return (3 * u) + v


total_cost2 = 0
for machine in machines:
    machine[-1] += 10000000000000
    machine[-2] += 10000000000000
    total_cost2 += min_cost_for_prize2(machine)
print(total_cost2)
