"""main

Description
===============================

This Python module is for running the project.
It will display a 2 by 2 rubik's cube.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Caleb Sadler.
"""
from __future__ import annotations
from math import pi
import pygame
import paint
import interaction
from cube import Cube


def initialize_screen(screen_size: tuple[int, int]) -> pygame.Surface:
    """Initialize pygame and the display window."""
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill((0, 0, 0))
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT])

    return screen


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


def run_sim() -> None:
    """Run simulation of 3d cube"""
    screen = initialize_screen((SCREEN_WIDTH, SCREEN_HEIGHT))
    cube1 = Cube((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 0), 70)
    solved_cube = Cube((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 0), 70)
    keys = paint.make_keys()

    bools = {
        'run': True,
        'scramble': False,
        'solve': False,
        'can_press': True,
        'up_down': True
    }

    nums = {
        'theta': pi / 500,
        'now_theta': 0,
        'axis': -10,
        'theta_thresh': 100,
        'solve_step': 0
    }

    strs = {
        'scramble_str': '',
        'solve_str': ''
    }

    buttons = {
        'n': (pygame.K_n, 0),
        't': (pygame.K_t, 1),
        'v': (pygame.K_v, 2),
        'j': (pygame.K_j, 3),
        'y': (pygame.K_y, 4),
        'f': (pygame.K_f, 5),
        'l': (pygame.K_LEFT, 6),
        'r': (pygame.K_RIGHT, 7),
    }

    while bools['run']:
        if bools['scramble']:    # if the scramble button is pressed
            interaction.handle_scramble(bools, nums, strs, buttons)
        elif bools['solve']:     # if the solve button is pressed
            interaction.handle_solve(cube1, solved_cube, [bools, nums, strs, buttons])
        else:   # otherwise check for rotation input
            interaction.handle_key_input(cube1, bools, nums, strs, buttons)

        interaction.handle_rotation(cube1, bools, nums)
        paint.draw_all(screen, cube1, keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bools['run'] = False

    pygame.display.quit()


if __name__ == "__main__":
    run_sim()
