#!/usr/bin/env python3

from .constants import NORTH, SOUTH, EAST, WEST
from .config import MazeConfig
from collections import deque

class MazeSolver:
    @staticmethod
    def solve(maze: list[list[int]], config: MazeConfig) -> str:
        directions = [((0, -1), "N", NORTH), ((1, 0), "E", EAST),
                      ((0, 1), "S", SOUTH), ((-1, 0), "W", WEST)]
        queue, discovered = deque(), {}
        came_from = {}

        queue.append(config.entry)
        discovered.add(config.entry)
        came_from[config.entry] = (None, "")

        while queue:
            curr_xy = queue.pop()
            curr_x, curr_y = curr_xy
            if curr_xy == config.exit: # Found
                return MazeSolver._reconstruct_path(came_from, config.exit)
            for (dx, dy), letter, bit in directions:
                next_xy = (curr_x + dx, curr_y + dy)
                if maze[curr_y][curr_x] & bit: # Wall
                    continue
                if next_xy in discovered: # Already discovered
                    continue
                queue.append(next_xy)
                discovered.add(next_xy)
                came_from[next_xy] = (curr_xy, letter)

        return ""
    
    @staticmethod
    def _reconstruct_path(came_from: dict, exit_pos: tuple[int, int]) -> str:
        pass
