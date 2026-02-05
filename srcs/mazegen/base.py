#!/usr/bin/env python3

import random
from .config import MazeConfig
from abc import ABC, abstractmethod


class MazeGeneratorBase(ABC):

    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.rng = random.Random(self.config.seed)
        self.grid = [[15 for _ in range(self.config.width)]
                     for _ in range(self.config.height)]

    @abstractmethod
    def generate(self):
        pass
