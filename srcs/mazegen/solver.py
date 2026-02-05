#!/usr/bin/env python3

from .constants import NORTH, SOUTH, EAST, WEST
from .config import MazeConfig
from collections import deque

class MazeSolver:
    @staticmethod
    def solve(maze: list[list[int]], config: MazeConfig) -> str:
        """BFS

        Attributes:
            queue (deque): coordinates to explore
            discovered (set): discovered coordinates
            parent (dict): {child_coordinate: (parent_coordinate, direction)}
        """
        directions = [
            ((0, -1), "N", NORTH),
            ((0, 1), "S", SOUTH),
            ((1, 0), "E", EAST),
            ((-1, 0), "W", WEST),
        ]
        queue, discovered = deque(), {}
        parent = {}

        queue.append(config.entry)
        discovered.add(config.entry)
        parent[config.entry] = (None, "")

        while queue:
            curr_xy = queue.pop()
            curr_x, curr_y = curr_xy

            # Found
            if curr_xy == config.exit:
                return ""

            for (dx, dy), letter, bit in directions:
                next_xy = (curr_x + dx, curr_y + dy)
                # Wall
                if maze[curr_x][curr_y] & bit:
                    continue
                # Already discovered
                if next_xy in discovered:
                    continue
                # Valid
                queue.append(next_xy)
                discovered.add(next_xy)
                parent[next_xy] = (curr_xy, letter)

        return ""
    

# x, y 入れ替える
# マクロ
# from enum import IntFlag <- 使う?