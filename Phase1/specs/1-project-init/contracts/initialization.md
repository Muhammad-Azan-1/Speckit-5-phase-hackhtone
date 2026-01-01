# API Contract: Project Initialization

## Overview
This contract defines the interface for initializing the Todo-CLI project with UV package manager.

## Initialization Command
- **Command**: `uv init --package ./todo-cli`
- **Purpose**: Create the initial project structure with proper Python packaging
- **Parameters**:
  - Directory name: `todo-cli`
  - Package name: `todo_cli`

## Expected Output
- Creates `todo-cli` directory
- Generates `pyproject.toml` with project configuration
- Creates `src/todo_cli/` package structure
- Sets up virtual environment management

## Dependencies Command
- **Command**: `uv add rich`
- **Purpose**: Add the rich package for enhanced terminal output
- **Parameters**:
  - Package name: `rich`

## Expected Output
- Adds rich to dependencies in pyproject.toml
- Installs rich in the virtual environment
- Updates lock file

## Execution Command
- **Command**: `uv run todo_cli`
- **Purpose**: Run the Todo-CLI application
- **Parameters**: None required for basic execution

## Expected Output
- Executes the CLI application
- Shows basic application functionality
- Returns exit code 0 on success