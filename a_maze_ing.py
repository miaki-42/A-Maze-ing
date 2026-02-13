#!/usr/bin/env python3

import argparse
from src.config_loader import load_config
from src.mazegen.maze_generator import MazeGenerator

if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()

    # Generate, Solve, Save
    try:
        mazegen = MazeGenerator(**load_config(args.file_path))
        maze = mazegen.generate()
        path = mazegen.shortest_path()
        mazegen.save()
    except Exception as e:
        print(f"Error: {e}")

    # Mlx


    # User interaction
    print(
        "=== A-Maze-ing ===\n"
        "1. Re-generate a new maze\n"
        "2. Show/Hide path from entry to exit\n"
        "3. Rotate maze colors\n"
        "4. Quit\n"
    )
    while True:
        choice = input("Choice? (1-4): ")
        match choice:
            case "1":
                print(mazegen.generate())
                print()
                print(mazegen.shortest_path())
            case "2":
                pass
            case "3":
                pass
            case "4":
                break
            case _:
                continue

