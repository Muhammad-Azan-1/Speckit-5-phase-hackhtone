"""Rich Output

This module provides the RichOutput class for formatting terminal output with colors and tables.
"""
from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing import List
from todo_cli.models.task import Task


class RichOutput:
    """Formatter for rich terminal output with colors and tables."""

    def __init__(self):
        """Initialize the RichOutput with a console instance."""
        self.console = Console()

    def format_task_list(self, tasks: List[Task]) -> str:
        """Format tasks as a rich table."""
        if not tasks:
            self.console.print("[cyan]No tasks found.[/cyan]")
            return ""

        # Create a table with columns: ID, Status, Description
        table = Table(title="Todo List")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Status", style="dim", width=12)
        table.add_column("Description", style="dim")

        for task in tasks:
            if task.status == "Completed":
                # Format completed tasks as dimmed with checkmark
                status_text = "[strikethrough][green]✓ Completed[/green][/strikethrough]"
                desc_text = f"[strikethrough]{task.description}[/strikethrough]"
                table.add_row(str(task.id), status_text, desc_text)
            else:
                # Format pending tasks as bright/bold
                table.add_row(str(task.id), "[blue]Pending[/blue]", f"[bold]{task.description}[/bold]")

        self.console.print(table)
        return ""

    def format_success_message(self, message: str) -> str:
        """Format success messages in green."""
        self.console.print(f"[green]{message}[/green]")
        return message

    def format_error_message(self, message: str) -> str:
        """Format error messages in bold red."""
        self.console.print(f"[bold red]{message}[/bold red]")
        return message

    def format_info_message(self, message: str) -> str:
        """Format info messages in blue/cyan."""
        self.console.print(f"[blue]{message}[/blue]")
        return message