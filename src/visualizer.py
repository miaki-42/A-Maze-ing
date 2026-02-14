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
        self.m.mlx_hook(self.win_ptr, XBUTTON, 0, self.close_window)
        self.m.mlx_key_hook(self.win_ptr, self.handle_keypress, self)
        # First draw
        self.draw_maze()

    def close_window(self) -> None:
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        sys.exit(0)

    def run(self) -> None:
        self.m.mlx_loop()

    def draw_maze(self) -> None:
        pass


    def draw_path(self) -> None:
        pass


    def handle_keypress(self) -> None:
        pass


    def regenerate(self) -> None:
        pass

    def rotate_wall_color(self) -> None:
        pass




# 4. メモリ（img_data）に直接ピクセルを書き込む
# 例: 画面全体を青色 (0x0000FF) で塗りつぶす
# 多くの環境では BGRA 順（Blue, Green, Red, Alpha）で並んでいます
for y in range(height):
    for x in range(width):
        # 1ピクセルあたりのバイトオフセットを計算
        offset = (y * size_line) + (x * (bpp // 8))
        
        # 青色 (Blue: 255, Green: 0, Red: 0) を書き込み
        img_data[offset] = 255     # Blue
        img_data[offset + 1] = 0   # Green
        img_data[offset + 2] = 0   # Red
        img_data[offset + 3] = 0   # Alpha (通常は無視されます)

# 5. 完成したイメージをウィンドウに一括転送
m.mlx_put_image_to_window(mlx_ptr, win_ptr, img_ptr, 0, 0)

