#!/usr/bin/env python3

from abc import ABC, abstractmethod
from random import Random
from .config import MazeConfig


class AbstractGeneratorAlgorithm(ABC):

    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.rng = Random(self.config.seed)
        self.grid = None

    @abstractmethod
    def generate(self):
        pass
