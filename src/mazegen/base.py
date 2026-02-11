#!/usr/bin/env python3

import random
from .config import MazeConfig
from abc import ABC, abstractmethod


class MazeGeneratorBase(ABC):

    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.rng = random.Random(self.config.seed)
        self.grid = None

    @abstractmethod
    def generate(self):
        pass

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

    def _is_safe_to_break(self, x: int, y: int, direction: int) -> bool:
        """
        壁を壊した結果、3x3の空き地ができないかチェック
        """
        for ox in range(x - 2, x + 1):
            for oy in range(y - 2, y + 1):

                if (ox < 0 or oy < 0 or ox + 2 >= self.config.width
                    or oy + 2 >= self.config.height):
                    continue

                if self._is_3x3_area_empty(ox, oy, x, y, direction):
                    return False

        return True

    def _is_3x3_area_empty(self, ox: int, oy: int, target_x: int,
                           target_y: int, target_dir: int) -> bool:
        """
        (ox, oy)を左上とする3x3エリア内の内部壁がすべてなくなっているか判定
        """
        internal_walls = []
        # 横方向
        for r in range(3):
            for c in range(2):
                internal_walls.append(((ox + c, oy + r), EAST))
        # 縦方向
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
        壁を壊して複数ルートを作る
        """
        extra_walls = (self.config.width * self.config.height) // 20
        broken = 0

        for _ in range(extra_walls * 5):
            if broken >= extra_walls:
                break

            tx = self.rng.randint(1, self.config.width - 2)
            ty = self.rng.randint(1, self.config.height - 2)
            direction = self.rng.choice([NORTH, EAST, SOUTH, WEST])

            if not (self.grid[ty][tx] & direction) or (self.grid[ty][tx] & VOID):
                continue

            if self._is_safe_to_break(tx, ty, direction):
                self._break_wall(tx, ty, direction)
                broken += 1
