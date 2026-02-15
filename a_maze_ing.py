#!/usr/bin/env python3

import sys
import argparse
from mazegen import MazeGenerator
from src.config_loader import load_config
from src.visualizer import MazeVisualizer


if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()

    # Generate Maze
    try:
        mazegen = MazeGenerator(**load_config(args.file_path))
        mazegen.generate()
        mazegen.save()
    except Exception as e:
        print(e)
        sys.exit(1)

    # User interaction
    print(
        "=== A-Maze-ing ===\n"
        "1. Re-generate a new maze\n"
        "2. Show/Hide path from entry to exit\n"
        "3. Rotate maze colors\n"
        "4. Quit\n"
    )

    # MLX
    visualizer = MazeVisualizer(mazegen)
    visualizer.run()
