# Quickstart Guide: Todo-CLI Project Setup

## Prerequisites
- UV package manager installed
- Python 3.13+ or higher available on your system

## Step 1: Install UV (if not already installed)
```bash
# Install UV using the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 2: Initialize the Project
```bash
# Initialize the Todo-CLI project
uv init --package ./todo-cli
```

## Step 3: Navigate to Project Directory
```bash
cd todo-cli
```

## Step 4: Add Required Dependencies
```bash
# Add the rich package for enhanced terminal output
uv add rich
```

## Step 5: Verify Setup
```bash
# Run the project to verify it's properly set up
uv run todo_cli
```

## Project Structure
After initialization, your project will have the following structure:
```
todo-cli/
├── pyproject.toml      # Project configuration and dependencies
├── uv.lock            # Dependency lock file
├── src/
│   └── todo_cli/
│       ├── __init__.py
│       └── main.py    # Entry point for the CLI application
├── tests/             # Test directory
├── README.md
└── .gitignore
```

## Next Steps
1. Implement the 5 core task management features:
   - Add Task
   - Delete Task
   - Update Task
   - View Task List
   - Mark as Complete
2. Add functionality to the main.py file
3. Create tests for your functionality