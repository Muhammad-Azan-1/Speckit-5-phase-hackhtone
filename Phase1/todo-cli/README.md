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
# Run the application
uv run todo-cli
```

## Dependencies

This project uses the `rich` package for enhanced terminal output with colors, panels, and formatting.

## Development

This project uses UV for package management and follows spec-driven development with Claude Code and Spec-Kit Plus.