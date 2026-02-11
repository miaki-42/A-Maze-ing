#!/usr/bin/env python3

import sys
from .config import MazeConfig
from .algorithms import DiggingGenerator
from .solver import MazeSolver

class MazeGenerator:
    # configを使う,seedも
    def __init__(self, width: int, height: int,
                 entry: tuple[int], exit: tuple[int],
                 output_file: str, perfect: bool, seed: int):
        self.config = MazeConfig(width=width, height=height, entry=entry, exit=exit,
                                 output_file=output_file, perfect=perfect, seed=seed)
        self.grid = None
        self.solution_path = None

    # 引数でアルゴリズム切り替え
    # listのlist,bitmap
    def generate(self) -> list[list[int]]:
        generator = DiggingGenerator(self.config)
        self.grid = generator.generate()
        self.solution_path = None
        return self.grid

    # ルート順を文字列で返す,n,e,s,w
    def solve(self) -> str | None:
        if self.grid is None:
            print("Error: Maze not generated yet. "
                  "Please call generate() before attempting to solve.",
                  file=sys.stderr)
            return None

        if self.solution_path is not None:
            return self.solution_path

        self.solution_path = MazeSolver.solve(self.grid, self.config)
        return self.solution_path

    def save(self) -> None:
        """
        迷路を指定された形式でファイルに出力します。
        """
        if self.grid is None:
            print("Error: Nothing to save.", file=sys.stderr)
            sys.exit(1)

        path = self.solve()

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
            print(f"Error saving to file: {e}", file=sys.stderr)
            sys.exit(1)
