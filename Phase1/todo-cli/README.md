# Todo-CLI

A command-line todo application with rich terminal output.

## Features

- Add tasks
- Delete tasks
- Update task details
- View task list
- Mark tasks as complete/incomplete
- Rich terminal output with colors and formatting

## Quick Start

1. **Prerequisites**: Install UV package manager and Python 3.13+
2. **Initialize Project**: Run `uv init --package ./todo-cli`
3. **Navigate**: Change to project directory with `cd todo-cli`
4. **Add Dependencies**: Run `uv add rich` to install rich package
5. **Run Project**: Execute `uv run todo_cli` to verify setup

## Installation

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the project directory
cd todo-cli

# Install dependencies
uv sync
```

## Usage

```bash
# Run the application (using the script name defined in pyproject.toml)
uv run todo-cli

# Or run as a Python module
uv run python -m todo_cli.main
```

## Available Commands

Once you run the application, you'll enter the Todo-CLI prompt (`todo> `). Here are all the available commands:

### Adding Tasks
```bash
# Add a new task
add <task description>
```
Example: `add Buy groceries for the week`

### Listing Tasks
```bash
# List all tasks in a formatted table
list
```

### Updating Tasks
```bash
# Update an existing task's description
update <task_id> <new_description>
```
Example: `update 1 Buy groceries for the month`

### Marking Tasks as Complete
```bash
# Mark a task as completed
complete <task_id>
```
Example: `complete 1`

### Deleting Tasks
```bash
# Delete a task
delete <task_id>
```
Example: `delete 1`

### Getting Help
```bash
# Show available commands
help
```

### Exiting the Application
```bash
# Exit the application
quit
# or
exit
```

## Command Details

- **add**: Creates a new task with the specified description. Task IDs are automatically assigned.
- **list**: Displays all tasks in a formatted table with their status (completed/incomplete), ID, and description.
- **update**: Changes the description of an existing task identified by its ID.
- **complete**: Marks a task as completed. Completed tasks will appear with a checkmark in the list.
- **delete**: Removes a task from the list permanently.
- **help**: Shows all available commands with brief descriptions.
- **quit/exit**: Exits the Todo-CLI application.

## Running the Application

There are several ways to run the Todo-CLI application:

### Method 1: Direct run with UV
```bash
uv run todo-cli
```

### Method 2: Install and run as a script
```bash
# Install in development mode
uv install --editables .

# Run the application
todo-cli
```

### Method 3: Run the module directly
```bash
uv run python -m todo_cli.main
```

## Dependencies

This project uses the `rich` package for enhanced terminal output with colors, panels, and formatting.

## Development

This project uses UV for package management and follows spec-driven development with Claude Code and Spec-Kit Plus.