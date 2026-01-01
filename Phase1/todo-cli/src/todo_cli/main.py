"""Todo-CLI Application Entry Point

This module provides the main entry point for the Todo-CLI application.
It initializes the application and starts the REPL interface.
"""
import sys
from todo_cli.cli.todo_cli import TodoCLI


def main():
    """Main entry point for the Todo-CLI application."""
    try:
        # Initialize and run the TodoCLI application
        cli = TodoCLI()
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()