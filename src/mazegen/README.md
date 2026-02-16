# Mazegen - Maze generation module
Standalone Python module designed to generate, solve and store complex mazes.

## Usage
You can install the package using the provided .whl or .tar.gz file. (pip install mazegen-1.0.0-py3-none-any.whl)  
Below is a simple usage example.
```
from mazegen import MazeGenerator

mazegen = MazeGenerator(
    width=20, height=15,
    entry=(0, 0), exit=(19, 14),
    output_file="maze.txt",
    perfect=True, seed=42
)

maze = mazegen.generate()
solution_path = mazegen.shortest_path()
mazegen.save()
```

## Parameter
- width(int) : Maze width (number of cells)
- height(int): Maze height
- entry(tuple[int, int]): Entry coordinates (x,y)
- exit(tuple[int, int]) : Exit coordinates (x,y)
- output_file(str): Output filename
- perfect(bool): Is the maze perfect?
- seed(Optional[int]): seed for random

## Generated Structure
Once the maze is generated, you can access its internal data directly through the object attributes.

### Grid (self.grid)
A 2D list of integers list[list[int]]  
Each integer (0–15) represents the walls of the cell using bitwise flags: North (1), East (2), South (4), and West (8). Cells belonging to the "42" pattern are marked with the value 31 for easy identification.

### Solution Path (self.solution_path)
A string consisting of 'N', 'E', 'S', 'W' representing the shortest valid path from entry to exit.
