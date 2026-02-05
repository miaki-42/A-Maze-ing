#!/usr/bin/env python3

from pydantic import BaseModel, Field, model_validator
from typing import Optional

class MazeConfig(BaseModel):
    width: int = Field(ge=7, description="Width of the maze (minimum 7)")
    height: int = Field(ge=5, description="Height of the maze (minimum 5)")
    entry: tuple[int, int] = Field(description="Entry point coordinates (x, y)")
    exit: tuple[int, int] = Field(description="Exit point coordinates (x, y)")
    output_file: str = Field(description="Output file path")
    perfect: bool = Field(description="Whether the maze is perfect (no loops)")
    seed: Optional[int] = Field(description="Random seed for maze generation")

    @model_validator(mode="after")
    def validate_coordinates(self) -> "MazeConfig":
        if self.entry[0] < 0 or self.entry[0] >= self.width:
            raise ValueError("Entry point x-coordinate is out of bounds")
        if self.entry[1] < 0 or self.entry[1] >= self.height:
            raise ValueError("Entry point y-coordinate is out of bounds")
        if self.exit[0] < 0 or self.exit[0] >= self.width:
            raise ValueError("Exit point x-coordinate is out of bounds")
        if self.exit[1] < 0 or self.exit[1] >= self.height:
            raise ValueError("Exit point y-coordinate is out of bounds")
        return self
