"""Todo Service

This module provides the TodoService class that manages in-memory task storage and operations.
"""
from typing import List, Dict
from todo_cli.models.task import Task
from datetime import datetime


class TodoService:
    """Service class that manages the in-memory task storage and operations."""

    def __init__(self):
        """Initialize the TodoService with an empty task dictionary and next_id counter."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Create a new task with auto-incrementing ID."""
        # Create a new task with the next available ID
        task_id = self.next_id
        self.next_id += 1

        # Create ISO 8601 timestamp in UTC
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Create the task
        task = Task(
            id=task_id,
            description=description,
            status="Pending",
            created_at=timestamp
        )

        # Add to tasks dictionary
        self.tasks[task_id] = task

        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by its ID."""
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found")
        return self.tasks[task_id]

    def validate_task_id(self, task_id: int) -> bool:
        """Check if a task ID exists."""
        return task_id in self.tasks

    def list_tasks(self) -> List[Task]:
        """Return all tasks in the system."""
        return list(self.tasks.values())

    def update_task(self, task_id: int, new_description: str) -> Task:
        """Update a task's description."""
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found")

        task = self.tasks[task_id]
        task.description = new_description
        task.validate()  # Re-validate after update
        return task

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as completed."""
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found")

        task = self.tasks[task_id]
        task.mark_completed()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Remove a task by its ID."""
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found")

        del self.tasks[task_id]
        return True