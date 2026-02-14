#!/usr/bin/env python3
"""
Main interface for maze generation, solving, and saving.
"""

import sys
from typing import Optional
from mazegen.config import MazeConfig
from mazegen.generator import DiggingGenerator
from mazegen.solver import BFSSolver


class MazeGenerator:
    """
    Main interface for maze generation, solving, and saving.
    """
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int], exit: tuple[int, int],
                 output_file: str, perfect: bool, seed: int):
        """
        Initialize the MazeGenerator with maze parameters and configuration.

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze.
            entry (tuple[int]): Entry coordinates.
            exit (tuple[int]): Exit coordinates.
            output_file (str): Output file path.
            perfect (bool): Whether the maze is perfect (no loops).
            seed (int): Random seed.
        """
        self.config = MazeConfig(
            width=width, height=height, entry=entry, exit=exit,
            output_file=output_file, perfect=perfect, seed=seed
        )
        self.generator = DiggingGenerator(self.config)
        self.solver = BFSSolver()
        self.grid: Optional[list[list[int]]] = None
        self.solution_path: Optional[str] = None

    def generate(self) -> list[list[int]]:
        """
        Generate a new maze and store the grid.

        Returns:
            list[list[int]]: The generated maze grid.
        """
        self.grid = self.generator.generate()
        self.solution_path = self.solver.solve()
        return self.grid

    def shortest_path(self) -> Optional[str]:
        """
        Find the shortest path in the maze.

        Returns:
            Optional[str]: The shortest path or None.
        """
        if self.grid is None:
            print("Error: Maze not generated yet. "
                  "Please call generate() before attempting to solve.",
                  file=sys.stderr)
            return None

        return self.solution_path

    def save(self) -> bool:
        """
        Save the maze to a file in the specified format.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.grid is None:
            print("Error: Nothing to save. "
                  "Please call generate() before attempting to save.",
                  file=sys.stderr)
            return False

        try:
            with open(self.config.output_file, 'w', encoding='utf-8') as f:
                for row in self.grid:
                    hex_row = "".join(f"{cell & 0xF:X}" for cell in row)
                    f.write(f"{hex_row}\n")
                f.write("\n")
                f.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
                f.write(f"{self.config.exit[0]},{self.config.exit[1]}\n")
                f.write(f"{self.solution_path}\n")
        except Exception as e:
            raise Exception(f"Error: saving to file {e}")

        return True
