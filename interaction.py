"""interaction

Description
===============================

This Python module is responsible for functions that lets
the user interact with the cube.

Copyright and Usage Information
===============================

This file is Copyright (c) 2020 Caleb Sadler.
"""
from __future__ import annotations
from math import pi
import random
import pygame
from cube import Cube


def handle_rotation(cube: Cube, bools: dict, nums: dict) -> None:
    """Handle calculations for rotating the cube"""
    if nums['now_theta'] >= nums['theta_thresh']:
        nums['now_theta'] = 0
        nums['theta_thresh'] = 100
        bools['can_press'] = True
        if nums['axis'] >= 0:
            cube.update_corners(nums['axis'])
        nums['axis'] = -10
    elif nums['axis'] >= 0:
        nums['now_theta'] += nums['theta']
        cube.relative_rotation(nums['theta'], nums['axis'])
    elif nums['axis'] == -1:
        nums['now_theta'] += nums['theta']
        cube.rotate_x(nums['theta'])
    elif nums['axis'] == -2:
        nums['now_theta'] += nums['theta']
        cube.rotate_x(-nums['theta'])


def handle_key_input(cube: Cube, bools: dict, nums: dict, strs: dict, buttons: dict) -> None:
    """Handle calculations for key input"""
    pressed = pygame.key.get_pressed()

    if bools['can_press'] and pressed[pygame.K_SPACE]:
        bools['scramble'] = True
        strs['scramble_str'] = get_scramble(buttons)
    elif bools['can_press'] and not cube.check_solve() and pressed[pygame.K_s]:
        bools['solve'] = True
        strs['solve_str'] = get_base(cube)
    elif bools['can_press'] and not bools['up_down'] and pressed[pygame.K_DOWN]:
        nums['axis'] = -1
        bools['up_down'] = True
        bools['can_press'] = False
        nums['theta_thresh'] = pi / 4
    elif bools['can_press'] and bools['up_down'] and pressed[pygame.K_UP]:
        nums['axis'] = -2
        bools['up_down'] = False
        bools['can_press'] = False
        nums['theta_thresh'] = pi / 4
    else:
        for button in buttons:
            if bools['can_press'] and pressed[buttons[button][0]]:
                nums['axis'] = buttons[button][1]
                bools['can_press'] = False
                nums['theta_thresh'] = pi / 2
                break


def handle_scramble(bools: dict, nums: dict, strs: dict, buttons: dict) -> None:
    """Handle calculations for scrambling the cube"""
    if strs['scramble_str'] == '':
        bools['can_press'] = False
        bools['scramble'] = False

    if bools['can_press']:
        nums['axis'] = buttons[strs['scramble_str'][0]][1]
        bools['can_press'] = False
        strs['scramble_str'] = strs['scramble_str'][1:]
        nums['theta_thresh'] = pi / 2


def get_scramble(buttons: dict) -> str:
    """Generate a string to scramble the cube"""
    scramble_str = ''

    for _ in range(0, 40):
        scramble_str += random.choice(list(buttons.keys()))

    return scramble_str


def handle_solve(cube: Cube, solved_cube: Cube, vals: list) -> None:
    """Handle calculations for solving the cube"""
    bools = vals[0]
    nums = vals[1]
    strs = vals[2]
    buttons = vals[3]
    if strs['solve_str'] == '':
        if cube.check_solve():  # if the cube is solved, reset and do nothing
            nums['solve_step'] = 0
            bools['solve'] = False
            bools['can_press'] = False
        elif bools['can_press'] and nums['solve_step'] == 0:  # orient the base corner
            nums['solve_step'] += 1
            strs['solve_str'] = get_orient(cube)
        elif bools['can_press'] and nums['solve_step'] >= 1:  # solve the cube
            nums['solve_step'] += 1
            strs['solve_str'] = get_solve(cube, solved_cube)

    if bools['can_press']:
        nums['axis'] = buttons[strs['solve_str'][0]][1]
        bools['can_press'] = False
        strs['solve_str'] = strs['solve_str'][1:]
        nums['theta_thresh'] = pi / 2


def get_base(cube: Cube) -> str:
    """Generate a string to move the base corner to the center"""
    solve_str = ''
    correct_colour = [(255, 255, 255), (0, 102, 204), (255, 0, 0)]

    corner_i = 0

    for corner in cube.corners:
        if corner.colours == correct_colour:
            corner_i = cube.corners.index(corner)
            break

    if corner_i == 0:
        solve_str = 'j'
    elif corner_i == 1:
        solve_str = 'llll'
    elif corner_i == 2:
        solve_str = 't'
    elif corner_i == 3:
        solve_str = 'jj'
    elif corner_i == 4:
        solve_str = 'ff'
    elif corner_i == 5:
        solve_str = 'y'
    elif corner_i == 6:
        solve_str = 'tt'
    elif corner_i == 7:
        solve_str = 'ljj'

    return solve_str


def get_orient(cube: Cube) -> str:
    """Generate a string to orient the base corner"""
    solve_str = ''
    correct_colour = [(255, 255, 255), (0, 102, 204), (255, 0, 0)]

    base_corner = None

    i = 0

    for corner in cube.corners:
        if corner.colours == correct_colour:
            base_corner = corner
            break
        i += 1

    if base_corner.colours[base_corner.col_index[0]] == correct_colour[0]:
        solve_str = 'llll'
    elif base_corner.colours[base_corner.col_index[0]] == correct_colour[1]:
        solve_str = 'fy'
    elif base_corner.colours[base_corner.col_index[0]] == correct_colour[2]:
        solve_str = 'jt'

    return solve_str


def get_solve(cube: Cube, solved_cube: Cube) -> str:
    """Generate a string to solve a corner"""
    solve_str = ''
    not_solved = []
    target_corner_i = 0
    col = [(255, 255, 0), (0, 102, 204), (255, 128, 0)]
    col_to_move = cube.corners[6].colours

    orientation_dict = {
        0: '',
        1: 'v',
        2: 'nn',
        3: 'nnv',
        4: 'f',
        5: 'ff',
        7: 'lyly',
    }

    for i in range(0, len(cube.corners)):
        if (cube.corners[i].colours != solved_cube.corners[i].colours
                or cube.corners[i].col_index != solved_cube.corners[i].col_index) and i != 6:
            not_solved.append(i)

    if cube.corners[6].colours == col:
        target_corner_i = random.choice(not_solved)
    else:
        for i in range(0, len(solved_cube.corners)):
            if solved_cube.corners[i].colours == col_to_move:
                target_corner_i = i
                break

    solve_str += orientation_dict[target_corner_i]

    if cube.corners[6].col_index[0] == 0:
        solve_str += ''
    elif cube.corners[6].col_index[0] == 1:
        solve_str += 'jv'
    elif cube.corners[6].col_index[0] == 2:
        solve_str += 'fn'

    reverse_str = make_reverse_algorithm(solve_str)
    solve_str += 'jynyjtnfjtnynvj'      # adding the algorithm to the current string
    solve_str += reverse_str
    solve_str += 'llll'

    return solve_str


def make_reverse_algorithm(solve_str: str) -> str:
    """Return a string that represents the reverse of the algorithm"""
    reverse_solve_str = ''

    reverse_map = {
        'n': 'j',
        't': 'y',
        'v': 'f',
        'j': 'n',
        'y': 't',
        'f': 'v',
        'l': 'r',
        'r': 'l'
    }

    for i in range(len(solve_str) - 1, -1, -1):
        reverse_solve_str += reverse_map[solve_str[i]]

    return reverse_solve_str


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['__future', 'math', 'random', 'pygame', 'cube', 'python_ta.contracts'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
