""" Fully Intractable 2 by 2 Rubik's Cube

Copyright (c) 2021 Caleb Sadler.
"""
from typing import Tuple
import pygame as pygame
from math import sin, cos, pi


class Corner:
    """Corner of a cube"""
    sides: list[list]
    origin: Tuple[float, float, float]
    colours: list[Tuple[int, int, int]]
    length: int

    def __init__(self, origin: Tuple[float, float, float], colours: list[Tuple[int, int, int]],
                 length: int, thetas: list[float]) -> None:
        """Initialize new corner of a cube"""
        self.origin = origin
        self.colours = colours
        self.length = length

        self.sides = [
            [(0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1)],
            [(0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 1, 1)],
            [(1, 0, 1), (1, 1, 1), (1, 1, 0), (1, 0, 0)]
        ]

        self.initial_rotate(thetas)
        self.multiply_points()

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

                r00 = x * (cos(theta) + vx ** 2 * (1 - cos(theta)))
                r01 = y * (vx * vy * (1 - cos(theta)) - vz * sin(theta))
                r02 = z * (vy * sin(theta) + vx * vz * (1 - cos(theta)))
                r10 = x * (vz * sin(theta) + vx * vy * (1 - cos(theta)))
                r11 = y * (cos(theta) + vy ** 2 * (1 - cos(theta)))
                r12 = z * (-vx * sin(theta) + vy * vz * (1 - cos(theta)))
                r20 = x * (-vy * sin(theta) + vx * vz * (1 - cos(theta)))
                r21 = y * (vx * sin(theta) + vy * vz * (1 - cos(theta)))
                r22 = z * (cos(theta) + vz ** 2 * (1 - cos(theta)))

                self.sides[side_i][point_i] = (
                    r00 + r01 + r02,
                    r10 + r11 + r12,
                    r20 + r21 + r22
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
    """Cube (2 by 2 Rubik's cube)"""
    origin: Tuple[float, float, float]
    corners: list[Corner]
    rotation_axes: list[tuple]
    rotation_corners: list[list]
    rotation_new_corners: list[list]
    length: int

    def __init__(self, origin: Tuple[float, float, float]) -> None:
        """Initialize a new cube"""
        self.origin = origin
        self.length = 80

        self.corners = [
            Corner(self.origin, [(255, 255, 0), (255, 0, 0), (0, 102, 204)], self.length, [pi, 3 * pi / 2]),
            Corner(self.origin, [(255, 255, 0), (0, 204, 0), (255, 0, 0)], self.length, [pi, pi]),
            Corner(self.origin, [(255, 255, 255), (255, 0, 0), (0, 204, 0)], self.length, [0, 3 * pi / 2]),
            Corner(self.origin, [(255, 255, 255), (0, 102, 204), (255, 0, 0)], self.length, [0, 0]),
            Corner(self.origin, [(255, 255, 0), (0, 102, 204), (255, 128, 0)], self.length, [pi, 0]),
            Corner(self.origin, [(255, 255, 0), (255, 128, 0), (0, 204, 0)], self.length, [pi, pi / 2]),
            Corner(self.origin, [(255, 255, 255), (0, 204, 0), (255, 128, 0)], self.length, [0, pi]),
            Corner(self.origin, [(255, 255, 255), (255, 128, 0), (0, 102, 204)], self.length, [0, pi / 2])
        ]

        self.rotation_axes = [
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
            (0, 1, 0),
            (0, -1, 0),
        ]

        self.rotation_corners = [
            [0, 1, 2, 3],
            [1, 2, 5, 6],
            [0, 1, 4, 5],
            [0, 1, 2, 3],
            [1, 2, 5, 6],
            [0, 1, 4, 5],
            [0, 1, 2, 3, 4, 5, 6, 7],
            [0, 1, 2, 3, 4, 5, 6, 7]
        ]

        self.rotation_new_corners = [
            [1, 2, 3, 0],
            [2, 6, 1, 5],
            [1, 5, 0, 4],
            [3, 0, 1, 2],
            [5, 1, 6, 2],
            [4, 0, 5, 1],
            [3, 2, 6, 7, 0, 1, 5, 4],
            [4, 5, 1, 0, 7, 6, 2, 3]
        ]

        self.rotate_y(pi / 4)
        self.rotate_x(pi / 8)

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

        for i in self.rotation_new_corners[axis]:
            corner_copies.append(self.corners[i])

        j = 0

        for i in self.rotation_corners[axis]:
            self.corners[i] = corner_copies[j]
            j += 1

    def rotate_x(self, theta: float) -> None:
        """Rotate cube around x"""
        for axis_i in range(0, len(self.rotation_axes)):
            x = self.rotation_axes[axis_i][0]
            y = self.rotation_axes[axis_i][1]
            z = self.rotation_axes[axis_i][2]

            self.rotation_axes[axis_i] = (
                x,
                y * cos(theta) + z * -sin(theta),
                y * sin(theta) + z * cos(theta)
            )

        for corner_i in range(0, len(self.corners)):
            self.corners[corner_i].rotate_x(theta)

    def rotate_y(self, theta: float) -> None:
        """Rotate cube around y"""
        for axis_i in range(0, len(self.rotation_axes)):
            x = self.rotation_axes[axis_i][0]
            y = self.rotation_axes[axis_i][1]
            z = self.rotation_axes[axis_i][2]

            self.rotation_axes[axis_i] = (
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
            self.corners[corner_i].relative_rotation(pi / 2, self.rotation_axes[1])

    def relative_rotation(self, theta: float, axis: int) -> None:
        """Rotate cube around vector"""
        for corner_i in range(0, len(self.corners)):
            if corner_i in self.rotation_corners[axis]:
                self.corners[corner_i].relative_rotation(theta, self.rotation_axes[axis])


def initialize_screen(screen_size: tuple[int, int]) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill((0, 0, 0))
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT])

    return screen


def run_sim() -> None:
    """Run simulation of 3d cube
    """
    run = True
    screen_width = 800
    screen_height = 800
    screen = initialize_screen((screen_width, screen_height))

    cube = Cube((screen_width / 2, screen_height / 2, 0))

    theta = pi / 500
    can_press = True
    now_theta = 0
    up_down = True
    axis = -10
    theta_thresh = 100

    while run:
        screen.fill((255, 255, 255))

        pressed = pygame.key.get_pressed()

        if can_press and pressed[pygame.K_n]:
            axis = 0
            can_press = False
            theta_thresh = pi / 2
        elif can_press and pressed[pygame.K_t]:
            axis = 1
            can_press = False
            theta_thresh = pi / 2
        elif can_press and pressed[pygame.K_v]:
            axis = 2
            can_press = False
            theta_thresh = pi / 2
        elif can_press and pressed[pygame.K_j]:
            axis = 3
            can_press = False
            theta_thresh = pi / 2
        elif can_press and pressed[pygame.K_y]:
            axis = 4
            can_press = False
            theta_thresh = pi / 2
        elif can_press and pressed[pygame.K_f]:
            axis = 5
            can_press = False
            theta_thresh = pi / 2
        elif can_press and pressed[pygame.K_LEFT]:
            axis = 6
            can_press = False
            theta_thresh = pi / 2
        elif can_press and pressed[pygame.K_RIGHT]:
            axis = 7
            can_press = False
            theta_thresh = pi / 2
        elif can_press and not up_down and pressed[pygame.K_DOWN]:
            axis = -1
            up_down = True
            can_press = False
            theta_thresh = pi / 4
        elif can_press and up_down and pressed[pygame.K_UP]:
            axis = -2
            up_down = False
            can_press = False
            theta_thresh = pi / 4
        elif now_theta >= theta_thresh:
            now_theta = 0
            theta_thresh = 100
            can_press = True
            if axis >= 0:
                cube.update_corners(axis)
            axis = -10
        elif axis >= 0:
            cube.relative_rotation(theta, axis)
            now_theta += theta
        elif axis == -1:
            cube.rotate_x(theta)
            now_theta += theta
        elif axis == -2:
            cube.rotate_x(-theta)
            now_theta += theta

        cube.visualize(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.display.quit()


if __name__ == "__main__":
    run_sim()
