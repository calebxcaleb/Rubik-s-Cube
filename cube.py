"""cube

Description
===============================

This Python module is a graph based Rubik's cub. It will
handle all the calculations to allow the user to interact
and see the Rubik's cube.

Copyright and Usage Information
===============================

This file is Copyright (c) 2020 Caleb Sadler.
"""
from __future__ import annotations
from typing import Tuple
from math import sin, cos, pi
import pygame


class Corner:
    """Corner of a cube

    A corner has three sides each with a different colour.
    Each corner has three neighbours, each face corresponding to a neighbour.
    """
    # Private Instance Attributes:
    #     - sides: list of positions for each face
    #     - origin: origin position of this corner in x, y, z
    #     - colours: list of colours for each face of the corner
    #     - col_index: mapping between the index of the colour and its original index
    #     - length: length of each side of the corner
    #     - neighbours: list of neighbours and coordinates of each face they are adjacent to
    #     - neighbour_index: the index of each neighbour in the Cube's corners list
    sides: list[list]
    origin: Tuple[float, float, float]
    colours: list[Tuple[int, int, int]]
    col_index: dict[int: int]
    length: int
    neighbours: list[list]
    neighbour_index: list[int]

    def __init__(self, origin: Tuple[float, float, float], colours: list[Tuple[int, int, int]],
                 length: int, thetas: list[float]) -> None:
        """Initialize new corner of a cube"""
        self.origin = origin
        self.colours = colours
        self.length = length
        self.col_index = {
            0: 0,
            1: 1,
            2: 2
        }

        self.sides = [
            [(0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1)],
            [(0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 1, 1)],
            [(1, 0, 1), (1, 1, 1), (1, 1, 0), (1, 0, 0)]
        ]

        self.initial_rotate(thetas)
        self.multiply_points()

    def check_solve(self) -> bool:
        """Check if the current corner is solved in relation to neighbouring corners"""
        for neighbour_info in self.neighbours:
            neighbour = neighbour_info[0]
            self_col = neighbour_info[1]
            other_col = neighbour_info[2]

            if not (self.colours[self_col[0]] == neighbour.colours[other_col[0]]
                    and self.colours[self_col[1]] == neighbour.colours[other_col[1]]):
                return False

        return True

    def multiply_points(self) -> None:
        """Multiply the points to the initial length
        """
        for side_i in range(0, len(self.sides)):
            for point_i in range(0, len(self.sides[side_i])):
                x = self.sides[side_i][point_i][0]
                y = self.sides[side_i][point_i][1]
                z = self.sides[side_i][point_i][2]

                self.sides[side_i][point_i] = [
                    x * self.length,
                    y * self.length,
                    z * self.length
                ]

    def initial_rotate(self, thetas: list[float]) -> None:
        """Rotate corner in given direction"""
        self.rotate_y(thetas[0])
        self.rotate_z(thetas[1])

    def rotate_x(self, theta: float) -> None:
        """Rotate corner around x"""
        for side_i in range(0, len(self.sides)):
            for point_i in range(0, len(self.sides[side_i])):
                x = self.sides[side_i][point_i][0]
                y = self.sides[side_i][point_i][1]
                z = self.sides[side_i][point_i][2]

                self.sides[side_i][point_i] = (
                    x,
                    y * cos(theta) + z * -sin(theta),
                    y * sin(theta) + z * cos(theta)
                )

    def rotate_y(self, theta: float) -> None:
        """Rotate corner around x"""
        for side_i in range(0, len(self.sides)):
            for point_i in range(0, len(self.sides[side_i])):
                x = self.sides[side_i][point_i][0]
                y = self.sides[side_i][point_i][1]
                z = self.sides[side_i][point_i][2]

                self.sides[side_i][point_i] = (
                    x * cos(theta) + z * sin(theta),
                    y,
                    x * -sin(theta) + z * cos(theta)
                )

    def rotate_z(self, theta: float) -> None:
        """Rotate corner around x"""
        for side_i in range(0, len(self.sides)):
            for point_i in range(0, len(self.sides[side_i])):
                x = self.sides[side_i][point_i][0]
                y = self.sides[side_i][point_i][1]
                z = self.sides[side_i][point_i][2]

                self.sides[side_i][point_i] = (
                    x * cos(theta) + y * -sin(theta),
                    x * sin(theta) + y * cos(theta),
                    z
                )

    def relative_rotation(self, theta: float, vector: tuple) -> None:
        """Rotate corner around given vector"""
        for side_i in range(0, len(self.sides)):
            for point_i in range(0, len(self.sides[side_i])):
                x = self.sides[side_i][point_i][0]
                y = self.sides[side_i][point_i][1]
                z = self.sides[side_i][point_i][2]
                vx = vector[0]
                vy = vector[1]
                vz = vector[2]

                r = [
                    [
                        x * (cos(theta) + vx ** 2 * (1 - cos(theta))),
                        y * (vx * vy * (1 - cos(theta)) - vz * sin(theta)),
                        z * (vy * sin(theta) + vx * vz * (1 - cos(theta)))
                    ],
                    [
                        x * (vz * sin(theta) + vx * vy * (1 - cos(theta))),
                        y * (cos(theta) + vy ** 2 * (1 - cos(theta))),
                        z * (-vx * sin(theta) + vy * vz * (1 - cos(theta)))
                    ],
                    [
                        x * (-vy * sin(theta) + vx * vz * (1 - cos(theta))),
                        y * (vx * sin(theta) + vy * vz * (1 - cos(theta))),
                        z * (cos(theta) + vz ** 2 * (1 - cos(theta)))
                    ]
                ]

                self.sides[side_i][point_i] = (
                    r[0][0] + r[0][1] + r[0][2],
                    r[1][0] + r[1][1] + r[1][2],
                    r[2][0] + r[2][1] + r[2][2]
                )

    def draw_sides(self, screen: pygame.Surface) -> None:
        """Draw each side of the corner"""
        index = 0
        side_list = []
        side_dict = {}

        for side in self.sides:
            side_list.append((side[0][2] + side[1][2] + side[2][2] + side[3][2]) / 4)
            side_dict[side_list[index]] = index
            index += 1

        side_list.sort(reverse=True)

        for i in range(0, len(side_list)):
            side = self.sides[side_dict[side_list[i]]]
            colour = self.colours[side_dict[side_list[i]]]
            rectangle = ((self.to_world(side[0])), self.to_world(side[1]),
                         self.to_world(side[2]), self.to_world(side[3]))
            pygame.draw.polygon(screen, colour, rectangle, 0)
            pygame.draw.polygon(screen, (0, 0, 0), rectangle, 5)

    def to_world(self, point: Tuple[float, float, float]) -> Tuple[float, float]:
        """Return 2d point given a 3d point
        """
        new_point = (point[0] + self.origin[0], point[1] + self.origin[1])
        return new_point


class Cube:
    """Cube (2 by 2 Rubik's cube)

    A cube has 8 corners.

    Instance Attributes
        - corners: a collection of corners in this cube (graph)
    """
    # Private Instance Attributes:
    #     - _origin: origin position of the cube in x, y, z
    #     - _rotation_axes: list of unit vectors that the cube
    #           is rotated around for each rotation
    #     - _rotation_corners: list of corners that are rotated
    #           for each rotation
    #     - _rotation_new_corners: the index for which each corner
    #           in _rotation_corners is mapped to
    #     - updated_corners: the reverse of _rotation_new_corners
    #     - _update_colours: list of new colour indices for when
    #           a corner is rotated
    corners: list[Corner]
    _origin: Tuple[float, float, float]
    _rotation_axes: list[tuple]
    _rotation_corners: list[list]
    _rotation_new_corners: list[list]
    _updated_corners: list[list]
    _update_colour: list[list[tuple]]

    def __init__(self, origin: Tuple[float, float, float], length: int) -> None:
        """Initialize a new cube"""
        self._origin = origin

        self.corners = [
            Corner(self._origin, [(255, 255, 255), (255, 0, 0), (0, 204, 0)],
                   length, [pi, 3 * pi / 2]),
            Corner(self._origin, [(255, 255, 255), (0, 102, 204), (255, 0, 0)],
                   length, [pi, pi]),
            Corner(self._origin, [(255, 255, 0), (255, 0, 0), (0, 102, 204)],
                   length, [0, 3 * pi / 2]),
            Corner(self._origin, [(255, 255, 0), (0, 204, 0), (255, 0, 0)],
                   length, [0, 0]),
            Corner(self._origin, [(255, 255, 255), (0, 204, 0), (255, 128, 0)],
                   length, [pi, 0]),
            Corner(self._origin, [(255, 255, 255), (255, 128, 0), (0, 102, 204)],
                   length, [pi, pi / 2]),
            Corner(self._origin, [(255, 255, 0), (0, 102, 204), (255, 128, 0)],
                   length, [0, pi]),
            Corner(self._origin, [(255, 255, 0), (255, 128, 0), (0, 204, 0)],
                   length, [0, pi / 2])
        ]

        self._rotation_axes = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
            (0, 1, 0),
            (0, -1, 0),
        ]

        self._rotation_corners = [
            [0, 1, 2, 3],
            [1, 2, 5, 6],
            [0, 1, 4, 5],
            [0, 1, 2, 3],
            [1, 2, 5, 6],
            [0, 1, 4, 5],
            [0, 1, 2, 3, 4, 5, 6, 7],
            [0, 1, 2, 3, 4, 5, 6, 7]
        ]

        self._rotation_new_corners = [
            [1, 2, 3, 0],
            [2, 6, 1, 5],
            [1, 5, 0, 4],
            [3, 0, 1, 2],
            [5, 1, 6, 2],
            [4, 0, 5, 1],
            [3, 2, 6, 7, 0, 1, 5, 4],
            [4, 5, 1, 0, 7, 6, 2, 3]
        ]

        self._updated_corners = [
            [3, 0, 1, 2],
            [5, 1, 6, 2],
            [4, 0, 5, 1],
            [1, 2, 3, 0],
            [2, 6, 1, 5],
            [1, 5, 0, 4],
            [4, 5, 1, 0, 7, 6, 2, 3],
            [3, 2, 6, 7, 0, 1, 5, 4]
        ]

        self._update_colour = [
            [(1, 2, 0), (2, 0, 1), (1, 2, 0), (2, 0, 1)],
            [(1, 2, 0), (2, 0, 1), (2, 0, 1), (1, 2, 0)],
            [(0, 1, 2), (0, 1, 2), (0, 1, 2), (0, 1, 2)],
            [(1, 2, 0), (2, 0, 1), (1, 2, 0), (2, 0, 1)],
            [(1, 2, 0), (2, 0, 1), (2, 0, 1), (1, 2, 0)],
            [(0, 1, 2), (0, 1, 2), (0, 1, 2), (0, 1, 2)],
            [(2, 0, 1), (1, 2, 0), (2, 0, 1), (1, 2, 0),
             (1, 2, 0), (2, 0, 1), (1, 2, 0), (2, 0, 1)],
            [(2, 0, 1), (1, 2, 0), (2, 0, 1), (1, 2, 0),
             (1, 2, 0), (2, 0, 1), (1, 2, 0), (2, 0, 1)]
        ]

        self.set_corner_neighbours()
        self.rotate_y(pi / 4)
        self.rotate_x(pi / 8)
        self.rotate_y(pi / 500)

    def set_corner_neighbours(self) -> None:
        """Set each corner to its correct neighbour"""
        self.corners[0].neighbours = [
            [self.corners[1], (0, 1), (0, 2)],
            [self.corners[3], (1, 2), (2, 1)],
            [self.corners[4], (2, 0), (1, 0)]
        ]
        self.corners[0].neighbour_index = [1, 3, 4]

        self.corners[1].neighbours = [
            [self.corners[5], (0, 1), (0, 2)],
            [self.corners[2], (1, 2), (2, 1)],
            [self.corners[0], (2, 0), (1, 0)]
        ]
        self.corners[1].neighbour_index = [5, 2, 0]

        self.corners[2].neighbours = [
            [self.corners[3], (0, 1), (0, 2)],
            [self.corners[1], (1, 2), (2, 1)],
            [self.corners[6], (2, 0), (1, 0)]
        ]
        self.corners[2].neighbour_index = [3, 1, 6]

        self.corners[3].neighbours = [
            [self.corners[7], (0, 1), (0, 2)],
            [self.corners[0], (1, 2), (2, 1)],
            [self.corners[2], (2, 0), (1, 0)]
        ]
        self.corners[3].neighbour_index = [7, 0, 2]

        self.corners[4].neighbours = [
            [self.corners[0], (0, 1), (0, 2)],
            [self.corners[7], (1, 2), (2, 1)],
            [self.corners[5], (2, 0), (1, 0)]
        ]
        self.corners[4].neighbour_index = [0, 7, 5]

        self.corners[5].neighbours = [
            [self.corners[4], (0, 1), (0, 2)],
            [self.corners[6], (1, 2), (2, 1)],
            [self.corners[1], (2, 0), (1, 0)]
        ]
        self.corners[5].neighbour_index = [4, 6, 1]

        self.corners[6].neighbours = [
            [self.corners[2], (0, 1), (0, 2)],
            [self.corners[5], (1, 2), (2, 1)],
            [self.corners[7], (2, 0), (1, 0)]
        ]
        self.corners[6].neighbour_index = [2, 5, 7]

        self.corners[7].neighbours = [
            [self.corners[6], (0, 1), (0, 2)],
            [self.corners[4], (1, 2), (2, 1)],
            [self.corners[3], (2, 0), (1, 0)]
        ]
        self.corners[7].neighbour_index = [6, 4, 3]

    def check_solve(self) -> bool:
        """Check if the current cube is solved"""
        for corner in self.corners:
            if not corner.check_solve():
                return False

        return True

    def visualize(self, screen: pygame.Surface) -> None:
        """Visualize the cube"""
        index = 0
        average_list = []
        average_dict = {}

        for corner in self.corners:
            side_list = []
            for side in corner.sides:
                side_list.append((side[0][2] + side[1][2] + side[2][2] + side[3][2]) / 4)
            average_list.append(max(side_list))
            average_dict[average_list[index]] = corner
            index += 1

        average_list.sort(reverse=True)

        for i in range(0, len(average_list)):
            corner = average_dict[average_list[i]]
            corner.draw_sides(screen)

    def update_corners(self, axis: int) -> None:
        """Update the positions of the corners"""
        corner_copies = []

        for i in self._rotation_new_corners[axis]:
            corner_copies.append(self.corners[i])

        change_neighbour = {}
        self.get_new_neighbour_info(axis, change_neighbour)
        self.update_neighbours(axis, change_neighbour)
        self.update_colours(axis, corner_copies)

    def get_new_neighbour_info(self, axis: int, change_neighbour: dict) -> None:
        """Get the neighbour information of each corner that moves in the rotation"""
        for i in self._rotation_corners[axis]:
            n = 0
            for index in self.corners[i].neighbour_index:
                if index in self._rotation_corners[axis]:
                    new_index = self._rotation_corners[axis].index(index)
                    self.corners[i].neighbour_index[n] = self._updated_corners[axis][new_index]
                else:
                    index_of_index = self.corners[i].neighbour_index.index(index)
                    change_neighbour[i] = (
                        index_of_index,
                        self.corners[i].neighbour_index[index_of_index],
                        self.corners[i].neighbours[index_of_index][0],
                        self.corners[i].neighbours[index_of_index][2]
                    )

                n += 1

    def update_neighbours(self, axis: int, change_neighbour: dict) -> None:
        """Update the neighbours of each corner"""
        if change_neighbour != {}:
            for i in self._rotation_corners[axis]:
                index = self._rotation_corners[axis].index(i)
                j = self._updated_corners[axis][index]
                var0 = change_neighbour[i][0]
                var1 = change_neighbour[j][1]
                var2 = change_neighbour[j][2]
                var3 = change_neighbour[j][3]
                new_colour_pos = (self.corners[i].neighbours[var0][1][1],
                                  self.corners[i].neighbours[var0][1][0])

                self.corners[var1].neighbours[self.corners[var1].neighbour_index.index(j)][0] = \
                    self.corners[i]
                self.corners[var1].neighbours[self.corners[var1].neighbour_index.index(j)][2] = \
                    new_colour_pos

                self.corners[i].neighbour_index[var0] = var1
                self.corners[i].neighbours[var0][0] = var2
                self.corners[i].neighbours[var0][2] = var3

    def update_colours(self, axis: int, corner_copies: list) -> None:
        """Update the neighbouring colours of each corner"""
        for j in range(0, len(self._rotation_corners[axis])):
            i = self._rotation_corners[axis][j]
            values = list(self.corners[i].col_index.values())
            i0 = values.index(0)
            i1 = values.index(1)
            i2 = values.index(2)

            self.corners[i].col_index[i0] = self._update_colour[axis][j][0]
            self.corners[i].col_index[i1] = self._update_colour[axis][j][1]
            self.corners[i].col_index[i2] = self._update_colour[axis][j][2]
            self.corners[i] = corner_copies[j]

    def rotate_x(self, theta: float) -> None:
        """Rotate cube around x"""
        for axis_i in range(0, len(self._rotation_axes)):
            x = self._rotation_axes[axis_i][0]
            y = self._rotation_axes[axis_i][1]
            z = self._rotation_axes[axis_i][2]

            self._rotation_axes[axis_i] = (
                x,
                y * cos(theta) + z * -sin(theta),
                y * sin(theta) + z * cos(theta)
            )

        for corner_i in range(0, len(self.corners)):
            self.corners[corner_i].rotate_x(theta)

    def rotate_y(self, theta: float) -> None:
        """Rotate cube around y"""
        for axis_i in range(0, len(self._rotation_axes)):
            x = self._rotation_axes[axis_i][0]
            y = self._rotation_axes[axis_i][1]
            z = self._rotation_axes[axis_i][2]

            self._rotation_axes[axis_i] = (
                x * cos(theta) + z * sin(theta),
                y,
                x * -sin(theta) + z * cos(theta)
            )

        for corner_i in range(0, len(self.corners)):
            self.corners[corner_i].rotate_y(theta)

    def rotate_z(self, theta: float) -> None:
        """Rotate cube around z"""
        for corner_i in range(0, len(self.corners)):
            self.corners[corner_i].rotate_z(theta)

    def rotate_whole_cube(self) -> None:
        """Rotate the whole rubik's cube"""
        for corner_i in range(0, len(self.corners)):
            self.corners[corner_i].relative_rotation(pi / 2, self._rotation_axes[1])

    def relative_rotation(self, theta: float, axis: int) -> None:
        """Rotate cube around vector"""
        for corner_i in range(0, len(self.corners)):
            if corner_i in self._rotation_corners[axis]:
                self.corners[corner_i].relative_rotation(theta, self._rotation_axes[axis])


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['annotations', 'typing', 'math', 'pygame', 'python_ta.contracts'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
