#!/usr/bin/env python3

import sys
from typing import Optional
from .config import MazeConfig
from .generator import DiggingGenerator
from .solver import BFSSolver


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 entry: tuple[int], exit: tuple[int],
                 output_file: str, perfect: bool, seed: int):
        self.config = MazeConfig(
            width=width, height=height, entry=entry, exit=exit,
            output_file=output_file, perfect=perfect, seed=seed
        )
        self.generator = DiggingGenerator(self.config)
        self.solver = BFSSolver()
        self.grid = None
        self.solution_path = None

    def generate(self) -> list[list[int]]:
        self.grid = self.generator.generate()
        self.solution_path = None
        return self.grid

    def shortest_path(self) -> Optional[str]:
        if self.grid is None:
            print("Error: Maze not generated yet. "
                  "Please call generate() before attempting to solve.",
                  file=sys.stderr)
            return None

        self.solution_path = self.solver.solve(self.grid, self.config)
        return self.solution_path

    def save(self) -> bool:
        """
        迷路を指定された形式でファイルに出力します。
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
