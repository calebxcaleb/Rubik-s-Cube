"""paint

Description
===============================

This Python module is printing necessary information to the pygame
window. It will display the rRubik's cube along with instructions.

Copyright and Usage Information
===============================

This file is Copyright (c) 2020 Caleb Sadler.
"""
from typing import Tuple
import pygame
import cube


def make_text(text: str, pos: tuple[int, int]) -> \
        Tuple[pygame.Surface, pygame.Rect, pygame.Rect]:
    """Draw the given text to the pygame screen at the given position.

    pos represents the *center* of the text.
    """
    font = pygame.font.SysFont('inconsolata', 45)
    text_surface = font.render(text, True, (0, 0, 0))
    width, height = text_surface.get_size()
    x_offset = 7
    y_offset = 5
    text_rect = pygame.Rect((pos[0] - width / 2, pos[1] - height / 2),
                            (pos[0] + width / 2, pos[1] + height / 2))
    box_rect = pygame.Rect((pos[0] - x_offset - width / 2, pos[1] - y_offset - height / 2),
                           (width + 2 * x_offset, height + 2 * y_offset))

    return (text_surface, text_rect, box_rect)


def make_keys() -> list:
    """Return  the text objects and rectangles for drawing"""
    return [
        make_text('T', (440, 140)),
        make_text('Y', (560, 140)),
        make_text('F', (325, 240)),
        make_text('V', (325, 360)),
        make_text('J', (675, 240)),
        make_text('N', (675, 360)),
        make_text('UP KEY', (500, 50)),
        make_text('DOWN KEY', (500, 500)),
        make_text('LEFT KEY', (120, 300)),
        make_text('RIGHT KEY', (880, 300)),
        make_text('S = solve', (100, 100)),
        make_text('Space = scramble', (800, 100))
    ]


def draw_keys(screen: pygame.Surface, keys: list) -> None:
    """Draw all the key inputs for the user to easily use the program"""
    for key in keys:
        pygame.draw.rect(screen, (100, 100, 250), key[2], 0)
        pygame.draw.rect(screen, (0, 0, 0), key[2], 3)
        screen.blit(key[0], key[1])


def draw_all(screen: pygame.Surface, cube1: cube.Cube, keys: list) -> None:
    """Draw all the necessary information to the screen"""
    if cube1.check_solve():  # if the cube is solved make background yellow
        screen.fill((255, 255, 0))
    else:  # otherwise make background white
        screen.fill((255, 255, 255))

    cube1.visualize(screen)
    draw_keys(screen, keys)
    pygame.display.flip()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['typing', 'pygame', 'cube', 'python_ta.contracts'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
