# Speckit-Plus Todo CLI Application

This repository contains a command-line todo application built with Python, using the Spec-Kit Plus framework for spec-driven development.

## Project Structure

- `.specify/` - Spec-Kit Plus templates and scripts
- `specs/` - Feature specifications and plans
- `history/` - Prompt History Records and Architecture Decision Records
- `todo-cli/` - The main Todo-CLI application code
- `CLAUDE.md` - Claude Code rules and instructions

## Todo-CLI Application

The main application is located in the `todo-cli/` directory. It's a command-line todo application with rich terminal output.

### Features

- Add, delete, update, and list tasks
- Mark tasks as complete/incomplete
- Rich terminal output with colors and formatting
- Interactive command-line interface

### Quick Start

1. Navigate to the todo-cli directory:
   ```bash
   cd todo-cli
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the application (using the script name defined in pyproject.toml):
   ```bash
   uv run todo-cli
   ```

   Or run as a Python module:
   ```bash
   uv run python -m todo_cli.main
   ```

### Available Commands

Once the application is running, you can use these commands:

- `add <description>` - Add a new task
- `list` - List all tasks
- `update <id> <description>` - Update a task's description
- `complete <id>` - Mark a task as completed
- `delete <id>` - Delete a task
- `help` - Show available commands
- `quit` or `exit` - Exit the application

For detailed usage instructions and all available options, see the [todo-cli/README.md](todo-cli/README.md) file.

## Development

This project uses:
- Python 3.13+
- UV package manager
- Rich library for terminal formatting
- Spec-Kit Plus for spec-driven development
- Claude Code for AI-assisted development