# Data Model: Todo API Endpoints

## Entities

### Task
- **id**: Integer - Primary key, auto-incrementing identifier
- **title**: String (1-255 characters) - Title of the task
- **description**: String (0-1000 characters) - Optional detailed description of the task
- **completed**: Boolean - Whether the task is completed or not
- **user_id**: String - Foreign key linking the task to a specific user
- **created_at**: DateTime (ISO 8601 format) - Timestamp when the task was created
- **updated_at**: DateTime (ISO 8601 format) - Timestamp when the task was last updated

### User
- **id**: String - Unique identifier for the user
- **email**: String - User's email address
- **name**: String - User's full name
- **created_at**: DateTime (ISO 8601 format) - Timestamp when the user account was created
- **updated_at**: DateTime (ISO 8601 format) - Timestamp when the user account was last updated

### Task List
- **tasks**: Array of Task objects - Collection of tasks belonging to a specific user
- **pagination**: Object - Metadata for pagination (page, limit, total_count)
- **filtering**: Object - Applied filters (status, date_range, etc.)
- **sorting**: Object - Applied sorting (field, direction)