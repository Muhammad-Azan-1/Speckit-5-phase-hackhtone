# Data Model: Task Management System

## Entity: Task

### Fields
- **id** (INTEGER)
  - PRIMARY KEY
  - AUTO_INCREMENT
  - Unique identifier for each task

- **title** (VARCHAR(200))
  - NOT NULL
  - VALIDATION: 1-200 characters
  - The main title/description of the task

- **description** (TEXT)
  - OPTIONAL
  - VALIDATION: max 1000 characters
  - Additional details about the task

- **completed** (BOOLEAN)
  - DEFAULT false
  - NOT NULL
  - Indicates whether the task is completed

- **user_id** (INTEGER)
  - FOREIGN KEY to users table
  - NOT NULL
  - Links the task to the user who created it

- **version** (INTEGER)
  - DEFAULT 1
  - NOT NULL
  - For optimistic locking to handle concurrent edits

- **created_at** (TIMESTAMP WITH TIME ZONE)
  - NOT NULL
  - Auto-generated on creation

- **updated_at** (TIMESTAMP WITH TIME ZONE)
  - NOT NULL
  - Auto-updates on modification

### Relationships
- **Task belongs to User** (Many-to-One)
  - A user can have many tasks
  - A task belongs to exactly one user
  - FOREIGN KEY: user_id references users.id
  - CASCADE DELETE: When user is deleted, all their tasks are deleted

### Constraints
- **NOT NULL constraints**: id, title, completed, user_id, created_at, updated_at
- **UNIQUE constraints**: None
- **CHECK constraints**:
  - title length between 1 and 200 characters
  - description length less than or equal to 1000 characters
- **INDEXES**:
  - Index on user_id (for efficient user-based queries)
  - Index on completed (for filtering by completion status)
  - Index on created_at (for sorting by creation date)

### Validation Rules
- Title must be between 1-200 characters (inclusive)
- Description, if provided, must be 1000 characters or less
- Completed field must be boolean (true/false)
- user_id must reference an existing user
- version field must be positive integer

### State Transitions
- **New Task**: created with completed = false, version = 1
- **Update Task**: version increments by 1 on each successful update
- **Complete Task**: completed field changes from false to true
- **Uncomplete Task**: completed field changes from true to false
- **Delete Task**: record removed from database

## Entity: User (Referenced)

### Fields (for reference only)
- **id** (INTEGER)
  - PRIMARY KEY
  - AUTO_INCREMENT
- **email** (VARCHAR)
  - UNIQUE
  - NOT NULL
- **name** (VARCHAR)
  - OPTIONAL
- **created_at** (TIMESTAMP WITH TIME ZONE)
  - NOT NULL
- **updated_at** (TIMESTAMP WITH TIME ZONE)
  - NOT NULL

## SQLModel Implementation

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id")

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    version: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)
    version: Optional[int] = Field(default=None)  # For optimistic locking
```

## Audit Trail Considerations
- The `version` field supports optimistic locking for concurrent edit detection
- The `updated_at` field provides timestamp information for change tracking
- Additional audit logging must be implemented at the application layer to track who made changes
- All task operations must be logged with user_id, timestamp, and action type as required by constitution Article 14