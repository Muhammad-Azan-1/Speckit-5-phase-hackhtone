# Quickstart Guide: Todo-CLI Basic Features

## Prerequisites
- Python 3.13+ or higher
- UV package manager
- Rich package installed (via dependencies)

## Running the Application

1. **Start the REPL**:
   ```bash
   python -m todo_cli.main
   ```
   This will start the interactive REPL with the prompt `todo> `

2. **Add a Task**:
   ```
   todo> add Buy milk
   ✅ Added 'Buy milk' (ID: 1)
   ```

3. **List Tasks**:
   ```
   todo> list
   [Displays formatted table with tasks]
   ```

4. **Complete a Task**:
   ```
   todo> complete 1
   Task 1 marked complete
   ```

5. **Update a Task**:
   ```
   todo> update 1 Buy whole milk
   Task 1 updated
   ```

6. **Delete a Task**:
   ```
   todo> delete 1
   🗑️ Deleted Task 1
   ```

7. **Exit the REPL**:
   ```
   todo> quit
   ```

## Available Commands

- `add <description>` - Add a new task
- `list` - List all tasks in formatted table
- `update <id> <new_description>` - Update task description
- `delete <id>` - Delete a task
- `complete <id>` - Mark task as completed
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Error Handling

- Invalid task IDs will show: "Error: ID <id> not found"
- Unknown commands will show: "Unknown command: <command>"
- Missing arguments will show: "Missing arguments for <command>"

## Expected Output Format

- Success messages appear in **green**
- Deletion messages appear in **red**
- Informational messages appear in **blue/cyan**
- Error messages appear in **bold red**
- Task list appears in a **formatted table** with color-coded status indicators