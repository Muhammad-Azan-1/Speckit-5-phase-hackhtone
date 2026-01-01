"""Todo CLI

This module provides the command-line interface for the Todo application using the cmd module.
"""
import cmd
from typing import List
from todo_cli.services.todo_service import TodoService
from todo_cli.output.rich_output import RichOutput


class TodoCLI(cmd.Cmd):
    """Command-line interface that handles user commands in the REPL."""

    def __init__(self):
        """Initialize the TodoCLI with service and output instances."""
        super().__init__()
        self.service = TodoService()
        self.output = RichOutput()
        self.prompt = "todo> "
        self.intro = "Welcome to Todo-CLI! Type 'help' for available commands."

    def do_add(self, line: str) -> bool:
        """Handles the add command: add <description>"""
        if not line.strip():
            self.output.format_error_message("Missing description for add command")
            return False

        try:
            # Validate description length (max 500 characters)
            if len(line) > 500:
                self.output.format_error_message("Error: Description too long. Maximum 500 characters.")
                return False

            # Add the task
            task = self.service.add_task(line)

            # Format and display success message
            message = f"✅ Added '{task.description}' (ID: {task.id})"
            self.output.format_success_message(message)
        except ValueError as e:
            self.output.format_error_message(f"Error: {str(e)}")
        except Exception as e:
            self.output.format_error_message(f"An error occurred while adding task: {str(e)}")

        return False  # Continue the REPL loop

    def do_list(self, line: str) -> bool:
        """Handles the list command: list"""
        try:
            tasks = self.service.list_tasks()
            self.output.format_task_list(tasks)
        except Exception as e:
            self.output.format_error_message(f"An error occurred while listing tasks: {str(e)}")

        return False  # Continue the REPL loop

    def do_complete(self, line: str) -> bool:
        """Handles the complete command: complete <id>"""
        if not line.strip():
            self.output.format_error_message("Missing ID for complete command")
            return False

        try:
            task_id = int(line.strip())

            # Validate task ID exists
            if not self.service.validate_task_id(task_id):
                self.output.format_error_message(f"Error: ID {task_id} not found")
                return False

            # Complete the task
            self.service.complete_task(task_id)

            # Format and display success message
            message = f"Task {task_id} marked complete"
            self.output.format_info_message(message)
        except ValueError:
            self.output.format_error_message(f"Error: Invalid task ID '{line.strip()}'")
        except Exception as e:
            self.output.format_error_message(f"An error occurred while completing task: {str(e)}")

        return False  # Continue the REPL loop

    def do_update(self, line: str) -> bool:
        """Handles the update command: update <id> <new_description>"""
        if not line.strip():
            self.output.format_error_message("Missing arguments for update command")
            return False

        try:
            # Split the line to extract ID and new description
            parts = line.split(' ', 1)
            if len(parts) != 2:
                self.output.format_error_message("Missing arguments for update command. Usage: update <id> <new_description>")
                return False

            task_id = int(parts[0])
            new_description = parts[1]

            # Validate task ID exists
            if not self.service.validate_task_id(task_id):
                self.output.format_error_message(f"Error: ID {task_id} not found")
                return False

            # Validate description length (max 500 characters)
            if len(new_description) > 500:
                self.output.format_error_message("Error: Description too long. Maximum 500 characters.")
                return False

            # Update the task
            self.service.update_task(task_id, new_description)

            # Format and display success message
            message = f"Task {task_id} updated"
            self.output.format_success_message(message)
        except ValueError:
            self.output.format_error_message(f"Error: Invalid task ID or description")
        except Exception as e:
            self.output.format_error_message(f"An error occurred while updating task: {str(e)}")

        return False  # Continue the REPL loop

    def do_delete(self, line: str) -> bool:
        """Handles the delete command: delete <id>"""
        if not line.strip():
            self.output.format_error_message("Missing ID for delete command")
            return False

        try:
            task_id = int(line.strip())

            # Validate task ID exists
            if not self.service.validate_task_id(task_id):
                self.output.format_error_message(f"Error: ID {task_id} not found")
                return False

            # Delete the task
            self.service.delete_task(task_id)

            # Format and display deletion message
            message = f"🗑️ Deleted Task {task_id}"
            self.output.format_error_message(message)  # Using error color (red) for deletion
        except ValueError:
            self.output.format_error_message(f"Error: Invalid task ID '{line.strip()}'")
        except Exception as e:
            self.output.format_error_message(f"An error occurred while deleting task: {str(e)}")

        return False  # Continue the REPL loop

    def do_quit(self, line: str) -> bool:
        """Handles the quit command: quit"""
        print("Goodbye!")
        return True  # Exit the REPL loop

    def do_exit(self, line: str) -> bool:
        """Handles the exit command: exit"""
        print("Goodbye!")
        return True  # Exit the REPL loop

    def default(self, line: str) -> bool:
        """Handle unknown commands."""
        command = line.split()[0] if line.split() else "unknown"
        self.output.format_error_message(f"Unknown command: {command}. Type 'help' for available commands")
        return False  # Continue the REPL loop

    def emptyline(self) -> bool:
        """Handle empty line input."""
        # Do nothing for empty lines, just continue the loop
        return False

    def do_help(self, arg: str) -> bool:
        """Override help to provide custom help messages."""
        if arg:
            # Show help for specific command
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    func = getattr(self, 'do_' + arg)
                    self.stdout.write(f'{str(func.__doc__)}\n')
                except AttributeError:
                    self.stdout.write(f'{arg}: No help available.\n')
            else:
                func()
        else:
            # Show general help
            self.stdout.write('Available commands:\n')
            self.stdout.write('  add <description>     - Add a new task\n')
            self.stdout.write('  list                  - List all tasks in formatted table\n')
            self.stdout.write('  update <id> <desc>    - Update task description\n')
            self.stdout.write('  delete <id>           - Delete a task\n')
            self.stdout.write('  complete <id>         - Mark task as completed\n')
            self.stdout.write('  help                  - Show available commands\n')
            self.stdout.write('  quit/exit             - Exit the application\n')

        return False