#!/usr/bin/env python3

import sys
from random import Random
from .constant import NORTH, EAST, SOUTH, WEST, VOID, PATTERN_42
from .abstract import AbstractGeneratorAlgorithm
from .config import MazeConfig

class DiggingGenerator(AbstractGeneratorAlgorithm):
    def __init__(self, config: MazeConfig) -> None:
        super().__init__(config)
        self.grid = DiggingGenerator._init_grid(
            self.config.width,
            self.config.height
        )

    def generate(self) -> list[list[int]]:

        self._apply_pattern_42()

        start_x, start_y = self.config.entry
        self._dig_iterative(start_x, start_y)

        return self.grid

    @staticmethod
    def _init_grid(width: int, height: int) -> list[list[int]]:
        return [[15 for _ in range(width)] for _ in range(height)]

    def _apply_pattern_42(self) -> None:

        p_height = len(PATTERN_42)
        p_width = len(PATTERN_42[0])

        if (self.config.width < p_width + 1
            or self.config.height < p_height + 1):

            print("Error: Maze is too small for the '42' pattern.",
                  file=sys.stderr)
            return

        offset_x = (self.config.width - p_width) // 2
        offset_y = (self.config.height - p_height) // 2

        target_coords = []
        forbidden_coords = {self.config.entry, self.config.exit}

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

                if (0 <= new_x < self.config.width and
                    0 <= new_y < self.config.height and
                    self.grid[new_y][new_x] == 15 and
                    not (self.grid[new_y][new_x] & VOID)):

                    self._break_wall(cur_x, cur_y, direction)
                    stack.append((new_x, new_y))
                    break

            else:
                stack.pop()
