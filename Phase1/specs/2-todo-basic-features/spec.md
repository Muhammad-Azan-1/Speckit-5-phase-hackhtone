# Feature Specification: Basic Todo Features with Color UI

**Feature Branch**: `2-todo-basic-features`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "# Specification: Basic Todo Features with Color UI

## 1. Feature Description

**Feature Name:** todo-basic-features

**Goal:** Implement the 5 core CRUD functionalities (Add, List, Update, Delete, Complete) for the In-Memory Todo CLI, enhanced with rich text output and color coding for better user experience.

**Value:** Provides the core utility of the application while satisfying the "User-Friendly" requirement via visual feedback (colors/tables).

## 2. User Scenarios

* **Add Task:** User runs `todo` to enter REPL, then types `add "Buy Milk"` → App prints "✅ Added 'Buy Milk' (ID: 1)" in **Green**.

* **List Tasks:** User runs `todo` to enter REPL, then types `list` → App displays a formatted **Table** showing ID, Description, Status.

    * Completed tasks appear **dimmed** or with a checkmark.

    * Pending tasks appear **bright/bold**.

* **Complete Task:** User runs `todo` to enter REPL, then types `complete 1` → App prints "Task 1 marked complete" in **Blue**.

* **Delete Task:** User runs `todo` to enter REPL, then types `delete 1` → App prints "🗑️ Deleted Task 1" in **Red**.

* **Error Handling:** User runs `todo` to enter REPL, then types `complete 99` (non-existent) → App prints "Error: ID 99 not found" in **Bold Red**.

## 3. Functional Requirements

### 3.1. Data Model (In-Memory)

* **Structure:** A simple `Task` class or dictionary containing:

    * `id` (int, auto-incrementing sequentially regardless of deletions)

    * `description` (str, max 500 characters)

    * `status` (enum: Pending, Completed)

    * `created_at` (timestamp in ISO 8601 format, UTC timezone)

* **Persistence:** None. Data resets when the app exits (Phase I Rule).

### 3.2. Command Interface

* **Add**: `add <description>`

* **List**: `list` (Displays table)

* **Update**: `update <id> <new_description>`

* **Delete**: `delete <id>`

* **Complete**: `complete <id>`

### 3.3. UI & Colors (The `rich` Library)

* MUST use the `rich` library for output.

* **Success Messages:** Green text.

* **Deletion/Destructive:** Red text.

* **Info/Status:** Blue or Cyan text.

* **List View:** Must render a `rich.table.Table` with columns: `ID`, `Status`, `Description`.

## 4. Technical Constraints (Constitution Check)

* **Language:** Python 3.13+

* **Location:** All code in `Todo-CLI/src/`.

* **Type Safety:** Strict typing for the `Task` model.

## 5. Success Criteria

* **Dependencies:** `uv sync` installs `rich` successfully.

* **Visual Validation:** Running `todo list` shows a aligned table, not just raw text.

* **Functionality:** All 5 commands work as expected in a single session.

* **Code Quality:** No global state pollution; logic is encapsulated in a `TodoService` class.

## 6. Assumptions

* Since this is In-Memory, the "State" is lost between command runs unless we implement an interactive REPL loop (e.g., `cmd` module or `rich` console loop).

* *Clarification assumed:* For Phase I, we will implement an **Interactive REPL** (running `python main.py` enters a `todo>` prompt) so the in-memory data persists during the session. If we used single CLI commands (like `python main.py add`), data would vanish immediately. I have give you a specifcation for finally creating the fully functioanl todo app you can update it if necessery for best result lets do write the specifcation  ultrathink"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task (Priority: P1)

As a user, I want to add new tasks to my todo list so that I can keep track of things I need to do.

**Why this priority**: This is the most fundamental operation that enables all other functionality.

**Independent Test**: Can be fully tested by adding a task and verifying it appears in the list with correct status and ID.

**Acceptance Scenarios**:

1. **Given** I am using the Todo-CLI application, **When** I run `todo add "Buy Milk"`, **Then** the application prints "✅ Added 'Buy Milk' (ID: 1)" in green text and the task is stored in memory
2. **Given** I have added tasks to the list, **When** I add another task, **Then** the new task gets the next sequential ID
3. **Given** I enter an empty description, **When** I run the add command, **Then** the application shows an appropriate error message

---

### User Story 2 - List Tasks (Priority: P1)

As a user, I want to view all my tasks in a formatted list so that I can see what I need to do and what I've completed.

**Why this priority**: This is the second most important operation that allows users to visualize their tasks.

**Independent Test**: Can be tested by adding tasks and then listing them to verify they appear correctly formatted with appropriate colors.

**Acceptance Scenarios**:

1. **Given** I have added tasks to the list, **When** I run `todo list`, **Then** the application displays a formatted table with columns: ID, Status, Description
2. **Given** I have both completed and pending tasks, **When** I list them, **Then** completed tasks appear dimmed with checkmarks while pending tasks appear bright/bold
3. **Given** I have no tasks, **When** I run the list command, **Then** the application shows an appropriate message

---

### User Story 3 - Complete Task (Priority: P2)

As a user, I want to mark tasks as complete so that I can track my progress and distinguish completed items.

**Why this priority**: Essential for task management functionality after basic CRUD operations are in place.

**Independent Test**: Can be tested by adding tasks, completing one, and then listing to verify the status has changed.

**Acceptance Scenarios**:

1. **Given** I have added tasks to the list, **When** I run `todo complete 1`, **Then** the application prints "Task 1 marked complete" in blue text and updates the task status
2. **Given** I try to complete a non-existent task, **When** I run `todo complete 99`, **Then** the application prints "Error: ID 99 not found" in bold red text
3. **Given** I have completed a task, **When** I list tasks, **Then** the completed task appears with appropriate formatting (dimmed/checkmark)

---

### User Story 4 - Delete Task (Priority: P2)

As a user, I want to remove tasks from my list so that I can keep my todo list clean and focused.

**Why this priority**: Important for maintaining a clean and manageable task list.

**Independent Test**: Can be tested by adding tasks, deleting one, and then listing to verify it's no longer present.

**Acceptance Scenarios**:

1. **Given** I have added tasks to the list, **When** I run `todo delete 1`, **Then** the application prints "🗑️ Deleted Task 1" in red text and removes the task from memory
2. **Given** I try to delete a non-existent task, **When** I run `todo delete 99`, **Then** the application prints "Error: ID 99 not found" in bold red text
3. **Given** I have deleted a task, **When** I list tasks, **Then** the deleted task no longer appears in the list

---

### User Story 5 - Update Task (Priority: P3)

As a user, I want to modify existing task descriptions so that I can correct errors or update details.

**Why this priority**: Useful for maintaining accurate task information, but less critical than core CRUD operations.

**Independent Test**: Can be tested by adding tasks, updating one, and then listing to verify the description has changed.

**Acceptance Scenarios**:

1. **Given** I have added tasks to the list, **When** I run `todo update 1 "Buy Whole Milk"`, **Then** the application updates the task description and confirms the change
2. **Given** I try to update a non-existent task, **When** I run `todo update 99 "New Description"`, **Then** the application prints "Error: ID 99 not found" in bold red text
3. **Given** I have updated a task, **When** I list tasks, **Then** the updated task appears with the new description

---

### Edge Cases

- What happens when trying to perform operations on a task ID that doesn't exist?
- How does the system handle very long task descriptions that might break the table formatting?
- What if the user provides insufficient arguments to a command (e.g., `update 1` without a new description)?
- How does the system handle special characters or emojis in task descriptions?
- How does the system handle completely invalid commands in the REPL (e.g., unknown commands)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an `add` command that accepts a task description and creates a new task with an auto-incrementing ID
- **FR-002**: System MUST provide a `list` command that displays all tasks in a formatted table with ID, Status, and Description columns
- **FR-003**: System MUST provide a `complete` command that marks a task as completed based on its ID
- **FR-004**: System MUST provide a `delete` command that removes a task based on its ID
- **FR-005**: System MUST provide an `update` command that modifies a task's description based on its ID
- **FR-006**: System MUST use the `rich` library for all console output with appropriate color coding
- **FR-007**: System MUST display success messages in green text
- **FR-008**: System MUST display deletion messages in red text
- **FR-009**: System MUST display status/info messages in blue or cyan text
- **FR-010**: System MUST display error messages in bold red text
- **FR-011**: System MUST store tasks in memory only (no persistent storage)
- **FR-012**: System MUST format completed tasks differently from pending tasks in the list view
- **FR-013**: System MUST validate task IDs exist before performing operations
- **FR-014**: System MUST provide appropriate error messages for invalid operations

### Key Entities *(include if feature involves data)*

- **Task**: Represents a single todo item with id, description, status (pending/completed), and creation timestamp
- **TodoService**: Service class that manages the in-memory task storage and operations
- **TaskList**: Collection of tasks managed by the TodoService

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 core commands (add, list, complete, delete, update) execute without errors in under 1 second each
- **SC-002**: The `list` command displays tasks in a properly formatted table with appropriate color coding
- **SC-003**: 100% of valid operations complete successfully without crashing the application
- **SC-004**: Error handling works correctly for all invalid operations with appropriate error messages
- **SC-005**: The application maintains consistent in-memory state during a single session
- **SC-006**: All rich text formatting and color coding displays correctly in the terminal

## Clarifications

### Session 2026-01-02

- Q: How should the command interface be implemented - as a REPL (interactive session) or as direct CLI commands? → A: REPL Model - Interactive session where users enter `todo>` prompt and then run commands like `add "Buy Milk"` without the `todo` prefix, which maintains in-memory state during the session.
- Q: How should the system handle task ID assignment after deletions? → A: Sequential - IDs continue to increment sequentially regardless of deletions (e.g., after deleting ID 2, next task gets ID 4).
- Q: How should the system handle completely invalid commands or malformed input in the REPL? → A: Specific Messages - Provide specific, helpful error messages for different types of invalid input (e.g., "Unknown command: invalidcommand", "Missing description for add command").
- Q: What format and timezone should be used for timestamps? → A: ISO 8601 UTC - Use ISO 8601 format in UTC timezone (e.g., "2026-01-02T10:30:00Z").
- Q: Should there be a maximum character limit for task descriptions? → A: Reasonable Limit - Set a reasonable limit like 500 characters to prevent UI issues while allowing detailed descriptions.