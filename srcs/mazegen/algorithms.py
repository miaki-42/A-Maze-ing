#!/usr/bin/env python3

import sys
from .config import MazeConfig
from .base import MazeGeneratorBase
from .constants import NORTH, SOUTH, EAST, WEST, VOID, PATTERN_42

class DiggingGenerator(MazeGeneratorBase):

    def __init__(self, config: MazeConfig) -> None:
        super().__init__(config)
        self.grid = [[15 for _ in range(self.config.width)]
                     for _ in range(self.config.height)]

    def _apply_pattern_42(self) -> None:

        p_height = len(PATTERN_42)
        p_width = len(PATTERN_42[0])

        if (self.config.width < p_width
            or self.config.height < p_height):

            print("Error: Maze is too small for the '42' pattern.",
                  file=sys.stderr)
            return

        offset_x = (self.config.width - p_width) // 2
        offset_y = (self.config.height - p_height) // 2

        for r, row_str in enumerate(PATTERN_42):
            for c, char in enumerate(row_str):
                if char == '#':
                    target_x = offset_x + c
                    target_y = offset_y + r

                    self.grid[target_y][target_x] |= VOID

    def _break_wall(self, x: int, y: int, direction: int) -> None:

        opposite = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: WEST,
            WEST: EAST
        }

        self.grid[y][x] &= ~direction

        nx, ny = x, y
        if direction == NORTH: ny -= 1
        elif direction == SOUTH: ny += 1
        elif direction == EAST: nx += 1
        elif direction == WEST: nx -= 1

        if 0 <= nx < self.config.width and 0 <= ny < self.config.height:
            self.grid[ny][nx] &= ~opposite[direction]

    def generate(self):
        self._apply_pattern_42()
