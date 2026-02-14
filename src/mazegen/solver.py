#!/usr/bin/env python3
"""
Maze solver using the Breadth-First Search (BFS) algorithm.
"""

from typing import Optional
from collections import deque
from mazegen.constant import NORTH, SOUTH, EAST, WEST
from mazegen.config import MazeConfig


class BFSSolver:
    """
    Maze solver using the BFS algorithm.
    """

    def solve(self, maze: list[list[int]], config: MazeConfig
              ) -> Optional[str]:
        """
        Solve the maze and return the shortest path as a string.

        Args:
            maze (list[list[int]]): The maze grid.
            config (MazeConfig): Maze configuration.

        Returns:
            Optional[str]: The shortest path as a string, or None if not found.
        """
        directions = [
            ((0, -1), "N", NORTH),
            ((1, 0), "E", EAST),
            ((0, 1), "S", SOUTH),
            ((-1, 0), "W", WEST)
        ]
        queue: deque[tuple[int, int]] = deque()
        discovered = set()
        came_from: dict[
            tuple[int, int], tuple[Optional[tuple[int, int]], str]
        ] = {}

        queue.append(config.entry)
        discovered.add(config.entry)
        came_from[config.entry] = (None, "")

        while queue:
            curr_xy = queue.popleft()
            curr_x, curr_y = curr_xy
            # Found
            if curr_xy == config.exit:
                return self._reconstruct_path(came_from, config.exit)
            for (dx, dy), letter, bit in directions:
                next_xy = (curr_x + dx, curr_y + dy)
                # Wall
                if maze[curr_y][curr_x] & bit:
                    continue
                # Already discovered
                if next_xy in discovered:
                    continue
                queue.append(next_xy)
                discovered.add(next_xy)
                came_from[next_xy] = (curr_xy, letter)

        return None

    def _reconstruct_path(
            self,
            came_from: dict[
                tuple[int, int], tuple[Optional[tuple[int, int]], str]
            ],
            exit: tuple[int, int]
    ) -> str:
        """
        Reconstruct the path from entry to exit.

        Args:
            came_from (dict): Dictionary of previous positions.
            exit (tuple[int, int]): Exit coordinates.

        Returns:
            str: The path as a string of directions.
        """
        moves = []
        curr_pos = exit
        while True:
            prev_pos, move_letter = came_from[curr_pos]
            if not prev_pos:
                break
            moves.append(move_letter)
            curr_pos = prev_pos
        return "".join(reversed(moves))
