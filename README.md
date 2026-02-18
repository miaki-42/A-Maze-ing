*This project has been created as part of the 42 curriculum by komatsuk, kkitagaw*

<br>

# Description
**A-Maze-ing** is a Python-based application designed for the algorithmic generation, solving, and visualization of mazes. The project automates the creation of grid-based structures through customizable configuration files and provides a suite of tools for both data export and interactive display.

<br>

# Instruction
Follow these steps to set up the environment and run the maze generator.
   
## 1. Environment Setup  
It is recommended to use a Python virtual environment to manage dependencies.
```
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate
```

In the 42 environment, the following command(s) must be executed in order to use MLX.
```
# 3. For mlx
./setting_mlx.sh
```

## 2. Installation
Use the provided Makefile to install necessary dependencies and the reusable mazegen module.
```
# 4. Install dependencies and the local module
make install
```

## 3. Execution
Once the installation is complete, you can run the program using the default configuration.
```
# 5. Run the program
make run
```

<br>

# Configuration File Format
The program requires a plain-text configuration file to define the maze parameters.  
The format follows these rules:
- Each line contains a single KEY=VALUE pair.
- Lines starting with # are treated as comments and ignored.
- Empty lines are allowed and ignored.

## Required Keys:
- WIDTH: The number of cells horizontally.
- HEIGHT: The number of cells vertically.
- ENTRY: The starting coordinates in (x,y) or x,y format.
- EXIT: The ending coordinates in (x,y) or x,y format.
- OUTPUT_FILE: The path where the generated maze data will be saved.
- PERFECT: Set to TRUE for a maze with a single path, or FALSE for a maze that may contain loops.
- SEED (Optional): An integer value for reproducible maze generation.

<br>

# Algorithm & Technical Choices
## Maze Generation Algorithm: Recursive Backtracker (Digging method)
The core generation logic employs a Recursive Backtracker using a **Digging method**. The process starts with a grid where all cells are separated by walls and proceeds by "digging" through these walls to visit unvisited cells, ensuring every part of the maze is connected.

## Why I chose this algorithm:
- **Constraint Compliance**: I selected this algorithm because it makes it easy to ensure that the generated maze is "perfect" (having a single path between any two points) and that all cells remain fully connected.

- **Open Space Prevention**: The digging method allows for straightforward integration of real-time checks during the generation process, making it simple to prevent the creation of open areas.

<br>

# Reusable Components
- **Maze Generation**: The MazeGenerator class and its underlying digging algorithm can be used to create maze structures in any Python-based application.

- **Pathfinding (Solver)**: The BFS-based solving logic is decoupled from the generator, allowing it to find the shortest path for any grid following the same data structure.

- **Output Management**: The logic for converting internal grid data into the standardized 4-bit hexadecimal format is fully reusable for data serialization.

## How to use
[Mazegen - Maze generation module](#mazegen---maze-generation-module)

# Team and Project Management
## Roles of Each Team Member
- kkitagaw: Focused on the core generation logic, including maze generation (Recursive Backtracker), configuration file parsing, and the hexadecimal file output system.

- komatsuk: Focused on the pathfinding algorithm (BFS), building the Makefile, documentation, graphical visualization using MLX, and overall project integration.

## Anticipated Planning and Evolution
Our project began with a collaborative session to deeply interpret the subject requirements. We jointly decided on the algorithms to be used and designed the overall class structure before writing any code. This initial investment in architectural planning allowed us to work independently on our respective modules with minimal integration conflicts.

## What Worked Well and What Could Be Improved
- **Successes**: The decision to spend significant time on the initial design phase was highly effective. Because the class interfaces and data structures were clearly defined at the start, we encountered no major logic errors or compatibility issues during the merging phase.

- **Improvements**: In hindsight, prioritizing the development of the MLX graphical interface would have been beneficial. Having a visual debugging tool earlier in the process would have made the validation of the generation and solving logic even smoother than it was with terminal-only feedback.

## Used specific tools
I’m not using any specific tools.

<br>

# Resources
## Reference
- **Algorithm Guidance**: A specific technical website was consulted to gain a visual and conceptual understanding of the Recursive Backtracker algorithm, which served as the foundation for the digging logic. -> [Algoful](https://algoful.com/Archive/Algorithm/MazeDig)

- **Graphical Implementation**: The official documentation for MiniLibX (MLX) was the sole resource used to implement window management, event handling, and the real-time rendering of the maze and its solution path.

## AI Usage
- **Architectural Collaboration**: When designing the class structure, we consulted AI for technical opinions to resolve design challenges during our discussions.

- **Translation & Web Browsing**: AI was used to supplement English proficiency for translation and served as a browsing assistant to gather technical information.

- **Refinement of Documentation**: AI assisted in refining docstrings and this README to ensure professional terminology.

<br>

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