#!/usr/bin/env python3

"""
Visualize mazes using the project's MLX framebuffer interface.

Provides MazeVisualizer which renders a MazeGenerator instance to an
MLX window and handles basic input for regeneration and display
options.
"""

import sys
from mazegen import MazeGenerator
from mlx import Mlx

MARGIN = 0.9

COLOR_BACKGROUND = 0x000000
COLOR_ENTRY = 0x00FF00
COLOR_EXIT = 0xFF0000
COLOR_PATH = 0xFFFF00
COLOR_42 = 0xFF00FF
COLOR_WALL = [0xFFFFFF, 0x00FFFF, 0xDAA520]

KEY_1, KEY_2, KEY_3, KEY_4 = 49, 50, 51, 52

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
VOID = 31


class MazeVisualizer:
    """
    Render a MazeGenerator to an MLX-based window.

    Args:
        maze: MazeGenerator used to build and solve the maze.
    """

    def __init__(self, maze: MazeGenerator) -> None:
        """
        Initialize visualizer and create MLX resources.

        Args:
            maze: MazeGenerator to visualize.
        """
        self.maze = maze
        self.width = self.maze.config.width
        self.height = self.maze.config.height
        self.entry = self.maze.config.entry
        self.exit = self.maze.config.exit
        # Flag
        self.show_path = True
        self.wall_color_ind = 0
        # Init Mlx
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        # Get window size
        _, w, h = self.m.mlx_get_screen_size(self.mlx_ptr)
        max_w, max_h = int(w * MARGIN), int(h * MARGIN)
        self.cellsize = min(max_w // self.width, max_h // self.height)
        if self.cellsize < 5:
            self.cellsize = 5
            print("Warning: Maze is too large")
        # Mlx Window
        self.win_w = self.width * self.cellsize
        self.win_h = self.height * self.cellsize
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, self.win_w, self.win_h, "A-Maze-ing"
        )
        self.img_ptr = self.m.mlx_new_image(
            self.mlx_ptr, self.win_w, self.win_h
        )
        self.data_addr, self.bpp, self.line_len, _ = (
            self.m.mlx_get_data_addr(self.img_ptr)
        )
        # Mlx Event
        self.m.mlx_key_hook(self.win_ptr, self.handle_keypress, self)
        # First draw
        self.draw_maze()

    def close_window(self, *args: "MazeVisualizer") -> None:
        """
        Close window, image and MLX loop.

        Args:
            *args: Hook callback arguments (ignored).
        """
        self.m.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_loop_exit(self.mlx_ptr)

    def handle_keypress(self, keycode: int, *args: "MazeVisualizer") -> None:
        """
        Handle key events for regeneration, display, and exit.

        Args:
            keycode: Integer key code from MLX hook.
            *args: Hook callback arguments (ignored).
        """
        if keycode == KEY_1:
            self.maze.generate()
            self.draw_maze()
        elif keycode == KEY_2:
            self.show_path = not self.show_path
            self.draw_maze()
        elif keycode == KEY_3:
            self.wall_color_ind = (self.wall_color_ind + 1) % len(COLOR_WALL)
            self.draw_maze()
        elif keycode == KEY_4:
            self.close_window()

    def run(self) -> None:
        """
        Enter the MLX event loop and exit the process on return.
        """
        self.m.mlx_loop(self.mlx_ptr)
        sys.exit(0)

    def draw_maze(self) -> None:
        """
        Render the maze to the MLX image and display it.
        """
        if self.maze.grid is None:
            raise ValueError("Error: maze.grid is None")
        for y in range(self.win_h):
            for x in range(self.win_w):
                self._put_pixel(y, x, COLOR_BACKGROUND)
        for y in range(self.height):
            for x in range(self.width):
                self._draw_wall(y, x)
                if self.maze.grid[y][x] == VOID:
                    self._fill_cell(y, x, COLOR_42, self.cellsize - 2)
        if self.show_path:
            self._draw_path()
        self._fill_cell(self.entry[1], self.entry[0],
                        COLOR_ENTRY, self.cellsize - 2)
        self._fill_cell(self.exit[1], self.exit[0],
                        COLOR_EXIT, self.cellsize - 2)
        self.m.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )

    def _draw_wall(self, y: int, x: int) -> None:
        """
        Draw cell walls for a given cell.

        Args:
            y: Row index of the cell.
            x: Column index of the cell.
        """
        if self.maze.grid is None:
            raise ValueError("Error: maze.grid is None")
        base_y, base_x = y * self.cellsize, x * self.cellsize
        ind = self.wall_color_ind
        if self.maze.grid[y][x] & NORTH:
            for i in range(self.cellsize):
                self._put_pixel(base_y, base_x + i, COLOR_WALL[ind])
        if self.maze.grid[y][x] & EAST:
            for i in range(self.cellsize):
                self._put_pixel(
                    base_y + i, base_x + self.cellsize - 1, COLOR_WALL[ind])
        if self.maze.grid[y][x] & SOUTH:
            for i in range(self.cellsize):
                self._put_pixel(
                    base_y + self.cellsize - 1, base_x + i, COLOR_WALL[ind])
        if self.maze.grid[y][x] & WEST:
            for i in range(self.cellsize):
                self._put_pixel(base_y + i, base_x, COLOR_WALL[ind])

    def _draw_path(self) -> None:
        """
        Draw the solver's solution path starting from the entry.
        """
        if self.maze.solution_path is None:
            raise ValueError("Error: maze.solution_path is None")
        pos_x, pos_y = self.entry
        for direction in self.maze.solution_path:
            if direction == "N":
                pos_y -= 1
            elif direction == "E":
                pos_x += 1
            elif direction == "S":
                pos_y += 1
            elif direction == "W":
                pos_x -= 1
            self._fill_cell(pos_y, pos_x, COLOR_PATH, self.cellsize // 4)

    def _fill_cell(self, y: int, x: int, color: int, size: int) -> None:
        """
        Fill a centered square inside a maze cell with color.

        Args:
            y: Row index of the cell.
            x: Column index of the cell.
            color: 24-bit RGB color value.
            size: Side length in pixels for the filled square.
        """
        base_y = y * self.cellsize + (self.cellsize - size) // 2
        base_x = x * self.cellsize + (self.cellsize - size) // 2
        for i in range(size):
            for j in range(size):
                self._put_pixel(base_y + i, base_x + j, color)

    def _put_pixel(self, y: int, x: int, color: int) -> None:
        """
        Write a 32-bit RGBA pixel into the image buffer.

        Args:
            y: Vertical pixel coordinate (row).
            x: Horizontal pixel coordinate (column).
            color: 24-bit RGB color value.
        """
        offset = (self.line_len * y) + (self.bpp // 8 * x)
        self.data_addr[offset] = color & 0xFF
        self.data_addr[offset + 1] = (color >> 8) & 0xFF
        self.data_addr[offset + 2] = (color >> 16) & 0xFF
        self.data_addr[offset + 3] = 0xFF
