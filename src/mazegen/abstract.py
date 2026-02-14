#!/usr/bin/env python3
"""
Abstract base class for maze generator algorithms.
"""

from abc import ABC, abstractmethod
from typing import Any
from random import Random
from mazegen.config import MazeConfig


class AbstractGeneratorAlgorithm(ABC):
    """
    Abstract base class for maze generator algorithms.
    """

    def __init__(self, config: MazeConfig) -> None:
        """
        Initialize with a MazeConfig object.

        Args:
            config (MazeConfig): Maze configuration object.
        """
        self.config = config
        self.rng = Random(self.config.seed)
        self.grid: list[list[int]]

    @abstractmethod
    def generate(self) -> Any:
        """
        Generate a maze grid. Must be implemented by subclasses.
        """
        pass
