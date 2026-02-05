#!/usr/bin/env python3

import random
from .config import MazeConfig
from abc import ABC, abstractmethod


class MazeGeneratorBase(ABC):

    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.rng = random.Random(self.config.seed)
        self.grid = None

    @abstractmethod
    def generate(self):
        pass
