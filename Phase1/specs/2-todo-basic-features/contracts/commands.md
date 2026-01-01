# API Contract: Todo CLI Commands

## Overview
This contract defines the command-line interface for the Todo-CLI application. The application uses a REPL model where users enter commands after a prompt.

## Command Interface
- **Prompt**: `todo> `
- **Exit commands**: `quit`, `exit`, or `Ctrl+D`
- **Help command**: `help` or `?` to show available commands

## Command Specifications

### Add Command
- **Command**: `add <description>`
- **Purpose**: Add a new task to the list
- **Parameters**:
  - `<description>`: Task description (string, max 500 characters)
- **Output**: "✅ Added '<description>' (ID: <id>)" in green text
- **Example**: `add Buy milk` → "✅ Added 'Buy milk' (ID: 1)"

### List Command
- **Command**: `list`
- **Purpose**: Display all tasks in a formatted table
- **Output**: Rich table with columns (ID, Status, Description)
- **Format**:
  - Pending tasks: bright/bold text
  - Completed tasks: dimmed with checkmark
- **Example**: `list` → formatted table of all tasks

### Complete Command
- **Command**: `complete <id>`
- **Purpose**: Mark a task as completed
- **Parameters**:
  - `<id>`: Task ID (integer)
- **Output**: "Task <id> marked complete" in blue text
- **Example**: `complete 1` → "Task 1 marked complete"

### Update Command
- **Command**: `update <id> <new_description>`
- **Purpose**: Update a task's description
- **Parameters**:
  - `<id>`: Task ID (integer)
  - `<new_description>`: New task description (string, max 500 characters)
- **Output**: "Task <id> updated" in green text
- **Example**: `update 1 Buy whole milk` → "Task 1 updated"

### Delete Command
- **Command**: `delete <id>`
- **Purpose**: Remove a task from the list
- **Parameters**:
  - `<id>`: Task ID (integer)
- **Output**: "🗑️ Deleted Task <id>" in red text
- **Example**: `delete 1` → "🗑️ Deleted Task 1"

## Error Handling

### Non-existent Task ID
- **Command**: Any command with invalid ID (e.g., `complete 99` when no task 99 exists)
- **Output**: "Error: ID <id> not found" in bold red text

### Invalid Command
- **Command**: Unknown command (e.g., `invalidcommand`)
- **Output**: "Unknown command: <command>. Type 'help' for available commands" in red text

### Missing Arguments
- **Command**: Command without required arguments (e.g., `add` without description)
- **Output**: "Missing arguments for <command>" in red text

### Description Too Long
- **Command**: Add or update with description over 500 characters
- **Output**: "Error: Description too long. Maximum 500 characters." in bold red text

## Output Formatting

### Success Messages
- **Color**: Green text
- **Examples**: Task added, updated, completed

### Deletion Messages
- **Color**: Red text
- **Examples**: Task deleted

### Info/Status Messages
- **Color**: Blue or cyan text
- **Examples**: Task marked complete

### Error Messages
- **Color**: Bold red text
- **Examples**: Invalid ID, command errors