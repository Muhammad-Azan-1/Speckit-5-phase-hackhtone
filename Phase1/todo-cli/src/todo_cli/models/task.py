"""Task Model

This module defines the Task entity with its attributes and validation methods.
"""
from dataclasses import dataclass
from typing import Literal
from datetime import datetime


@dataclass
class Task:
    """Represents a single todo item in the application."""

    id: int
    description: str
    status: Literal["Pending", "Completed"]
    created_at: str  # ISO 8601 format in UTC timezone

    def __post_init__(self):
        """Validate the Task attributes after initialization."""
        self.validate()

    def validate(self):
        """Validate the task attributes."""
        # Validate ID is a positive integer
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError(f"ID must be a positive integer, got {self.id}")

        # Validate description length (max 500 characters)
        if not isinstance(self.description, str):
            raise ValueError(f"Description must be a string, got {type(self.description)}")
        if len(self.description) > 500:
            raise ValueError(f"Description must be 500 characters or less, got {len(self.description)} characters")

        # Validate status is either "Pending" or "Completed"
        if self.status not in ["Pending", "Completed"]:
            raise ValueError(f"Status must be 'Pending' or 'Completed', got '{self.status}'")

        # Validate created_at is in ISO 8601 format
        try:
            # Try to parse the datetime to ensure it's in valid ISO 8601 format
            datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Created_at must be in ISO 8601 format, got '{self.created_at}'")

    def mark_completed(self):
        """Mark the task as completed."""
        self.status = "Completed"