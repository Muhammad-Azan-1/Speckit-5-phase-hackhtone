# Implementation Tasks: Basic Todo Features with Color UI

**Feature**: Basic Todo Features with Color UI
**Branch**: 2-todo-basic-features
**Created**: 2026-01-02
**Status**: Draft
**Priority Order**: P1 → P2 → P3 (User Story priority from spec.md)

## Dependencies

- User Story 2 (List Tasks) requires User Story 1 (Add Task) components to be tested
- User Stories 3, 4, 5 (Complete, Delete, Update) require User Story 1 (Add Task) components
- All UI features depend on foundational Task model and TodoService

## Implementation Strategy

**MVP Scope**: User Story 1 (Add Task) with minimal List functionality for verification

**Incremental Delivery**:
1. Phase 1-2: Foundation (Task model, TodoService, basic REPL)
2. Phase 3: User Story 1 (Add Task) - P1 priority
3. Phase 4: User Story 2 (List Tasks) - P1 priority
4. Phase 5: User Story 3 (Complete Task) - P2 priority
5. Phase 6: User Story 4 (Delete Task) - P2 priority
6. Phase 7: User Story 5 (Update Task) - P3 priority
7. Phase 8: Polish & cross-cutting concerns

## Phase 1: Setup

### Goal
Initialize the project structure for the Todo-CLI application with proper file organization and basic configuration.

### Independent Test Criteria
- Can run the application via `python -m todo_cli.main`
- Application displays REPL prompt
- Basic command structure is in place

### Tasks

- [ ] T001 Create src/todo_cli directory structure
- [ ] T002 Create main.py file with basic application entry point
- [ ] T003 Add rich as dependency in pyproject.toml if not already present

## Phase 2: Foundational Components

### Goal
Implement the core data model and service layer that will support all user stories.

### Independent Test Criteria
- Can create Task objects with proper attributes and validations
- TodoService can store and retrieve tasks
- RichOutput can format basic messages with colors

### Tasks

- [ ] T004 [P] Create Task model in src/todo_cli/models/task.py with id, description, status, created_at attributes
- [ ] T005 [P] Implement Task validation methods (description length, status enum, ID validation)
- [ ] T006 [P] Create TodoService class in src/todo_cli/services/todo_service.py with tasks dict and next_id counter
- [ ] T007 [P] Implement TodoService.add_task() method with auto-incrementing ID
- [ ] T008 [P] Implement TodoService.get_task() and TodoService.validate_task_id() methods
- [ ] T009 [P] Implement TodoService.list_tasks() method
- [ ] T010 [P] Implement TodoService.update_task(), complete_task(), and delete_task() methods
- [ ] T011 [P] Create RichOutput class in src/todo_cli/output/rich_output.py
- [ ] T012 [P] Implement RichOutput.format_success_message() method with green text
- [ ] T013 [P] Implement RichOutput.format_error_message() method with bold red text
- [ ] T014 [P] Implement RichOutput.format_info_message() method with blue/cyan text
- [ ] T015 [P] Implement RichOutput.format_task_list() method with Rich table formatting

## Phase 3: User Story 1 - Add Task (Priority: P1)

### Goal
Implement the ability for users to add new tasks to their todo list with appropriate success messaging.

### Independent Test Criteria
- Can run `todo add "Buy Milk"` and see "✅ Added 'Buy Milk' (ID: 1)" in green text
- Added task is stored in memory with correct ID and status
- Subsequent tasks get next sequential ID

### Tasks

- [ ] T016 [P] [US1] Create do_add method in TodoCLI class to handle add command
- [ ] T017 [P] [US1] Parse description from command line in do_add method
- [ ] T018 [P] [US1] Validate description length (max 500 characters) in do_add
- [ ] T019 [US1] Call TodoService.add_task() from do_add method
- [ ] T020 [US1] Format and display success message using RichOutput.format_success_message()
- [ ] T021 [US1] Handle empty description error case with appropriate error message

## Phase 4: User Story 2 - List Tasks (Priority: P1)

### Goal
Implement the ability for users to view all their tasks in a formatted list with appropriate visual styling.

### Independent Test Criteria
- Can run `todo list` and see a formatted table with ID, Status, Description columns
- Pending tasks appear bright/bold
- Completed tasks appear dimmed with checkmarks
- Empty list shows appropriate message

### Tasks

- [ ] T022 [P] [US2] Create do_list method in TodoCLI class to handle list command
- [ ] T023 [P] [US2] Call TodoService.list_tasks() from do_list method
- [ ] T024 [US2] Format task list using RichOutput.format_task_list()
- [ ] T025 [US2] Implement proper styling for pending tasks (bright/bold)
- [ ] T026 [US2] Implement proper styling for completed tasks (dimmed/checkmark)
- [ ] T027 [US2] Handle empty task list case with appropriate message

## Phase 5: User Story 3 - Complete Task (Priority: P2)

### Goal
Implement the ability for users to mark tasks as complete with appropriate status messaging.

### Independent Test Criteria
- Can run `todo complete 1` and see "Task 1 marked complete" in blue text
- Task status changes from "Pending" to "Completed"
- Completed task appears with appropriate formatting when listed

### Tasks

- [ ] T028 [P] [US3] Create do_complete method in TodoCLI class to handle complete command
- [ ] T029 [P] [US3] Parse task ID from command line in do_complete method
- [ ] T030 [US3] Validate task ID exists using TodoService.validate_task_id()
- [ ] T031 [US3] Call TodoService.complete_task() from do_complete method
- [ ] T032 [US3] Format and display success message using RichOutput.format_info_message()
- [ ] T033 [US3] Handle invalid task ID error case with appropriate error message

## Phase 6: User Story 4 - Delete Task (Priority: P2)

### Goal
Implement the ability for users to remove tasks from their list with appropriate deletion messaging.

### Independent Test Criteria
- Can run `todo delete 1` and see "🗑️ Deleted Task 1" in red text
- Task is removed from memory
- Deleted task no longer appears when listing tasks

### Tasks

- [ ] T034 [P] [US4] Create do_delete method in TodoCLI class to handle delete command
- [ ] T035 [P] [US4] Parse task ID from command line in do_delete method
- [ ] T036 [US4] Validate task ID exists using TodoService.validate_task_id()
- [ ] T037 [US4] Call TodoService.delete_task() from do_delete method
- [ ] T038 [US4] Format and display deletion message using RichOutput.format_error_message() (red text)
- [ ] T039 [US4] Handle invalid task ID error case with appropriate error message

## Phase 7: User Story 5 - Update Task (Priority: P3)

### Goal
Implement the ability for users to modify existing task descriptions with appropriate update messaging.

### Independent Test Criteria
- Can run `todo update 1 "Buy Whole Milk"` and see confirmation message
- Task description is updated in memory
- Updated task appears with new description when listed

### Tasks

- [ ] T040 [P] [US5] Create do_update method in TodoCLI class to handle update command
- [ ] T041 [P] [US5] Parse task ID and new description from command line in do_update method
- [ ] T042 [US5] Validate task ID exists using TodoService.validate_task_id()
- [ ] T043 [US5] Validate new description length (max 500 characters) in do_update
- [ ] T044 [US5] Call TodoService.update_task() from do_update method
- [ ] T045 [US5] Format and display success message using RichOutput.format_success_message()
- [ ] T046 [US5] Handle invalid task ID error case with appropriate error message

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Complete the REPL interface with proper command handling, error management, and user experience enhancements.

### Independent Test Criteria
- All commands work as specified in the contracts
- Invalid commands show appropriate error messages
- REPL handles Ctrl+D and exit/quit commands properly
- All error scenarios from spec work correctly

### Tasks

- [ ] T047 Create TodoCLI class in src/todo_cli/cli/todo_cli.py extending cmd.Cmd
- [ ] T048 Implement proper REPL loop with "todo> " prompt
- [ ] T049 Implement do_quit and do_exit methods for quitting the application
- [ ] T050 Implement default method to handle unknown commands with appropriate error message
- [ ] T051 Handle missing arguments for commands with appropriate error messages
- [ ] T052 Implement proper command parsing for descriptions with spaces/quotes
- [ ] T053 Add help commands (do_help) for all implemented commands
- [ ] T054 Update main.py to initialize and run TodoCLI with TodoService and RichOutput
- [ ] T055 Test all error handling scenarios from the specification
- [ ] T056 Verify all color formatting works correctly in terminal
- [ ] T057 Run full integration test of all 5 commands in sequence