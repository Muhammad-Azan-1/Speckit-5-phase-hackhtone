# Data Model: Basic Todo Features

## Entity: Task

**Name**: Task
**Description**: Represents a single todo item in the application
**Attributes**:
- `id`: int (auto-incrementing sequentially regardless of deletions)
- `description`: str (max 500 characters)
- `status`: str (enum: "Pending", "Completed")
- `created_at`: str (ISO 8601 format, UTC timezone)

**Validations**:
- Description must be 500 characters or less
- Status must be either "Pending" or "Completed"
- ID must be a positive integer

**State Transitions**:
- From "Pending" to "Completed" when the task is completed
- No transition back from "Completed" to "Pending" (as per requirements)

**Relationships**:
- Belongs to: TodoService (contained in the tasks collection)

## Entity: TodoService

**Name**: TodoService
**Description**: Service class that manages the in-memory task storage and operations
**Attributes**:
- `tasks`: dict (collection of Task objects keyed by ID)
- `next_id`: int (class-level counter for auto-incrementing IDs)

**Methods**:
- `add_task(description: str) -> Task`: Creates a new task with auto-incrementing ID
- `get_task(task_id: int) -> Task`: Retrieves a task by its ID
- `list_tasks() -> List[Task]`: Returns all tasks in the system
- `update_task(task_id: int, new_description: str) -> Task`: Updates a task's description
- `complete_task(task_id: int) -> Task`: Marks a task as completed
- `delete_task(task_id: int) -> bool`: Removes a task by its ID
- `validate_task_id(task_id: int) -> bool`: Checks if a task ID exists

**Relationships**:
- Contains: Multiple Task entities
- Used by: TodoCLI (command-line interface)

## Entity: TodoCLI

**Name**: TodoCLI
**Description**: Command-line interface that handles user commands in the REPL
**Attributes**:
- `service`: TodoService (reference to the service layer)
- `prompt`: str (the prompt string to display, e.g., "todo> ")

**Methods**:
- `do_add(line: str) -> bool`: Handles the add command
- `do_list(line: str) -> bool`: Handles the list command
- `do_update(line: str) -> bool`: Handles the update command
- `do_delete(line: str) -> bool`: Handles the delete command
- `do_complete(line: str) -> bool`: Handles the complete command
- `do_quit(line: str) -> bool`: Handles the quit command

**Relationships**:
- Uses: TodoService for business logic
- Outputs: Rich-formatted responses to console

## Entity: RichOutput

**Name**: RichOutput
**Description**: Formatter for rich terminal output with colors and tables
**Methods**:
- `format_task_list(tasks: List[Task]) -> str`: Formats tasks as a rich table
- `format_success_message(message: str) -> str`: Formats success messages in green
- `format_error_message(message: str) -> str`: Formats error messages in bold red
- `format_info_message(message: str) -> str`: Formats info messages in blue/cyan

**Relationships**:
- Used by: TodoCLI for formatted output
- Depends on: Rich library