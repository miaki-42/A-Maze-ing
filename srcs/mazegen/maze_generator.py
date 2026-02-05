#!/usr/bin/env python3

from .config import MazeConfig
from .algorithms import
from .solver import MazeSolver

class MazeGenerator:
    # configを使う,seedも
    def __init__(self):
        pass

    # 引数でアルゴリズム切り替え
    # listのlist,bitmap
    def generate(self) -> list:
        pass

    # ルート順を文字列で返す,n,e,s,w
    def solver(self) -> str:
        pass