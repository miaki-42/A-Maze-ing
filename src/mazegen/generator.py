#!/usr/bin/env python3
"""
Maze generator using the digging (DFS) algorithm
"""

import sys
from mazegen.constant import NORTH, EAST, SOUTH, WEST, VOID, PATTERN_42
from mazegen.abstract import AbstractGeneratorAlgorithm


class DiggingGenerator(AbstractGeneratorAlgorithm):
    """
    Maze generator using the digging (DFS) algorithm.
    """

    def generate(self) -> list[list[int]]:
        """
        Generate a maze grid using the digging algorithm.

        Returns:
            list[list[int]]: The generated maze grid.
        """
        self.grid = DiggingGenerator._init_grid(
            self.config.width, self.config.height
        )
        self._apply_pattern_42()
        self._dig_iterative(*self.config.entry)
        if not self.config.perfect:
            self._add_loops()
        return self.grid

    @staticmethod
    def _init_grid(width: int, height: int) -> list[list[int]]:
        """
        Initialize the maze grid with all walls present (value 15).

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze.

        Returns:
            list[list[int]]: Initialized grid.
        """
        return [[15 for _ in range(width)] for _ in range(height)]

    def _apply_pattern_42(self) -> None:
        """
        Apply the '42' pattern to the maze grid if the maze is large enough.
        Outputs an error if the pattern overlaps with entry or exit.
        """
        p_height, p_width = len(PATTERN_42), len(PATTERN_42[0])
        if (self.config.width <= p_width or self.config.height <= p_height):
            print("Error: Maze is too small for the '42' pattern.",
                  file=sys.stderr)
            return

        target_coords = []
        forbidden_coords = {self.config.entry, self.config.exit}
        offset_x = (self.config.width - p_width) // 2
        offset_y = (self.config.height - p_height) // 2

        for r, row_str in enumerate(PATTERN_42):
            for c, char in enumerate(row_str):
                if char == '#':
                    target_x = offset_x + c
                    target_y = offset_y + r
                    if (target_x, target_y) in forbidden_coords:
                        print("Error: '42' pattern overlaps with Entry/Exit.",
                              file=sys.stderr)
                        return
                    target_coords.append((target_x, target_y))

        for target_x, target_y in target_coords:
            self.grid[target_y][target_x] |= VOID

    def _dig_iterative(self, start_x: int, start_y: int) -> None:
        """
        Iteratively dig paths in the maze using DFS from the start position.

        Args:
            start_x (int): X coordinate to start digging.
            start_y (int): Y coordinate to start digging.
        """
        stack = [(start_x, start_y)]

        while stack:
            cur_x, cur_y = stack[-1]
            directions = [NORTH, EAST, SOUTH, WEST]
            self.rng.shuffle(directions)

            for direction in directions:
                new_x, new_y = cur_x, cur_y
                if direction == NORTH:
                    new_y -= 1
                elif direction == SOUTH:
                    new_y += 1
                elif direction == EAST:
                    new_x += 1
                elif direction == WEST:
                    new_x -= 1

                if (
                    0 <= new_x < self.config.width
                    and 0 <= new_y < self.config.height
                    and self.grid[new_y][new_x] == 15
                    and not (self.grid[new_y][new_x] & VOID)
                ):
                    self._break_wall(cur_x, cur_y, direction)
                    stack.append((new_x, new_y))
                    break
            else:
                stack.pop()

    def _break_wall(self, x: int, y: int, direction: int) -> None:
        """
        Break the wall in the given direction.

        Args:
            x (int): X coordinate of the cell.
            y (int): Y coordinate of the cell.
            direction (int): Direction to break the wall.
        """
        opposite = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: WEST,
            WEST: EAST
        }

        self.grid[y][x] &= ~direction

        nx, ny = x, y
        if direction == NORTH:
            ny -= 1
        elif direction == SOUTH:
            ny += 1
        elif direction == EAST:
            nx += 1
        elif direction == WEST:
            nx -= 1

        if 0 <= nx < self.config.width and 0 <= ny < self.config.height:
            self.grid[ny][nx] &= ~opposite[direction]

    def _is_safe_to_break(self, x: int, y: int, direction: int) -> bool:
        """
        Check if breaking a wall will not create a 3x3 empty area.

        Args:
            x (int): X coordinate of the cell.
            y (int): Y coordinate of the cell.
            direction (int): Direction to check.

        Returns:
            bool: True if safe, False otherwise.
        """
        for ox in range(x - 2, x + 1):
            for oy in range(y - 2, y + 1):

                if (
                    ox < 0 or oy < 0 or ox + 2 >= self.config.width
                    or oy + 2 >= self.config.height
                ):
                    continue

                if self._is_3x3_area_empty(ox, oy, x, y, direction):
                    return False

        return True

    def _is_3x3_area_empty(self, ox: int, oy: int, target_x: int,
                           target_y: int, target_dir: int) -> bool:
        """
        Check if all internal walls in a 3x3 area are gone.

        Args:
            ox (int): X coordinate of the top-left of the 3x3 area.
            oy (int): Y coordinate of the top-left of the 3x3 area.
            target_x (int): X coordinate of the target cell.
            target_y (int): Y coordinate of the target cell.
            target_dir (int): Direction of the target wall.

        Returns:
            bool: True if the area is empty, False otherwise.
        """
        internal_walls = []
        # Horizontal walls
        for r in range(3):
            for c in range(2):
                internal_walls.append(((ox + c, oy + r), EAST))
        # Vertical walls
        for r in range(2):
            for c in range(3):
                internal_walls.append(((ox + c, oy + r), SOUTH))

        for (wx, wy), wdir in internal_walls:

            if wx == target_x and wy == target_y and wdir == target_dir:
                continue

            if self.grid[wy][wx] & wdir:
                return False

        return True

    def _add_loops(self) -> None:
        """
        Break additional walls to create multiple routes in the maze.
        """
        extra_walls = (self.config.width * self.config.height) // 10
        broken = 0

        for _ in range(extra_walls * 3):
            if broken >= extra_walls:
                break

            tx = self.rng.randint(0, self.config.width - 1)
            ty = self.rng.randint(0, self.config.height - 1)
            (dx, dy), direction = self.rng.choice([
                ((0, -1), NORTH),
                ((1, 0), EAST),
                ((0, 1), SOUTH),
                ((-1, 0), WEST)
            ])

            if (
                not (self.grid[ty][tx] & direction)
                or (self.grid[ty][tx] & VOID)
            ):
                continue
            new_x, new_y = tx + dx, ty + dy
            if (
                not (0 <= new_x < self.config.width)
                or not (0 <= new_y < self.config.height)
                or self.grid[new_y][new_x] & VOID
            ):
                continue

            if self._is_safe_to_break(tx, ty, direction):
                self._break_wall(tx, ty, direction)
                broken += 1
