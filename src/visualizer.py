#!/usr/bin/env python3

import sys
from mazegen import MazeGenerator
from mlx import Mlx

CELLSIZE = 16

COLOR_BACKGROUND = 0x000000
COLOR_ENTRY = 0x00FF00
COLOR_EXIT = 0xFF0000
COLOR_PATH = 0xFFFF00
COLOR_42 = 0xFF00FF
COLOR_WALL = [0xFFFFFF, 0x00FFFF, 0xDAA520]

XBUTTON = 17
KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_4 = 52

class MazeVisualizer:

    def __init__(self, maze: MazeGenerator) -> None:
        # Maze
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
        # Mlx Window
        self.win_w = self.width * CELLSIZE
        self.win_h = self.height * CELLSIZE
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

    # Attention to arguments, loop_exit
    def close_window(self, *args) -> None:
        self.m.mlx_destroy_image(self.mlx_ptr, self.img_ptr)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_loop_exit(self.mlx_ptr)

    # Attention to arguments
    def handle_keypress(self, keycode: int, *args) -> None:
        if keycode == KEY_1:
            pass
        elif keycode == KEY_2:
            pass
        elif keycode == KEY_3:
            pass
        elif keycode == KEY_4:
            self.close_window()

    def run(self) -> None:
        self.m.mlx_loop(self.mlx_ptr)
        sys.exit(0)

    def draw_maze(self) -> None:
        # process
        self.m.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )


    def draw_path(self) -> None:
        pass

    def regenerate(self) -> None:
        pass

    def rotate_wall_color(self) -> None:
        pass

