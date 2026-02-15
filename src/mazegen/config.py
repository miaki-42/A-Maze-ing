#!/usr/bin/env python3
"""
Maze configuration model for maze generation settings.
"""

from typing import Optional
from pydantic import BaseModel, Field, model_validator


class MazeConfig(BaseModel):
    """
    Configuration model for maze generation.
    """
    width: int = Field(ge=1, description="Width of the maze")
    height: int = Field(ge=1, description="Height of the maze")
    entry: tuple[int, int] = Field(description="Entry point coordinates (x,y)")
    exit: tuple[int, int] = Field(description="Exit point coordinates (x,y)")
    output_file: str = Field(description="Output file path")
    perfect: bool = Field(description="Whether the maze is perfect (no loops)")
    seed: Optional[int] = Field(
        default=None, description="Random seed for maze generation")

    @model_validator(mode="after")
    def validate_coordinates(self) -> "MazeConfig":
        """
        Validate entry and exit coordinates.
        """
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        if entry_x < 0 or entry_x >= self.width:
            raise ValueError("Entry point x-coordinate is out of bounds")
        if entry_y < 0 or entry_y >= self.height:
            raise ValueError("Entry point y-coordinate is out of bounds")
        if exit_x < 0 or exit_x >= self.width:
            raise ValueError("Exit point x-coordinate is out of bounds")
        if exit_y < 0 or exit_y >= self.height:
            raise ValueError("Exit point y-coordinate is out of bounds")
        if entry_x == exit_x and entry_y == exit_y:
            raise ValueError("Entry and exit points cannot be the same")
        return self
