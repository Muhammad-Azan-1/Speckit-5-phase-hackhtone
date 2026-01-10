# Data Model: Todo Dashboard

## Entity Definitions

### 1. Task
- **Purpose**: Represents a user's todo item
- **Fields**:
  - `id`: INTEGER, PRIMARY KEY, AUTO_INCREMENT (auto-generated primary key)
  - `title`: STRING(200), NOT NULL, CHECK LENGTH(1-200) (task title)
  - `description`: TEXT, OPTIONAL, CHECK LENGTH(0-1000) (task description)
  - `completed`: BOOLEAN, NOT NULL, DEFAULT FALSE (completion status)
  - `user_id`: STRING(255), FOREIGN KEY, NOT NULL (owner of the task)
  - `category_id`: INTEGER, FOREIGN KEY, OPTIONAL (associated category)
  - `created_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT NOW() (creation timestamp)
  - `updated_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT NOW() (last update timestamp)

- **Relationships**:
  - `user_id` → `user.id` (many-to-one with users table)
  - `category_id` → `category.id` (many-to-one with categories table)

- **Validation Rules**:
  - Title: 1-200 characters
  - Description: 0-1000 characters
  - user_id must reference valid user
  - category_id must reference valid category (if provided)

### 2. Category
- **Purpose**: Represents a task category with emoji icon
- **Fields**:
  - `id`: INTEGER, PRIMARY KEY, AUTO_INCREMENT (auto-generated primary key)
  - `name`: STRING(50), NOT NULL (category name)
  - `icon`: STRING(10), NOT NULL (emoji icon for category)
  - `user_id`: STRING(255), FOREIGN KEY, NOT NULL (owner of the category)
  - `created_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT NOW() (creation timestamp)

- **Relationships**:
  - `user_id` → `user.id` (many-to-one with users table)
  - `category.id` → `task.category_id` (one-to-many with tasks table)

- **Validation Rules**:
  - Name: 1-50 characters
  - Icon: Must be a valid emoji (single emoji character or emoji sequence)
  - user_id must reference valid user

### 3. User Profile
- **Purpose**: Represents user account information (extends Better Auth user)
- **Fields**:
  - `user_id`: STRING(255), PRIMARY KEY, FOREIGN KEY (reference to Better Auth user)
  - `name`: STRING(255) (display name, overrides Better Auth name)
  - `avatar_url`: STRING(500), OPTIONAL (custom avatar URL)
  - `preferences`: JSON, OPTIONAL (user preferences including theme, date format, etc.)
  - `created_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT NOW() (account creation)
  - `updated_at`: TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT NOW() (last update)

- **Relationships**:
  - `user_id` → `user.id` (one-to-one with Better Auth users table)

### 4. Dashboard Stats
- **Purpose**: Aggregated statistics for dashboard display (computed view)
- **Computed Fields**:
  - `total_tasks`: INTEGER (count of all user's tasks)
  - `completed_tasks`: INTEGER (count of completed tasks)
  - `pending_tasks`: INTEGER (count of pending tasks)
  - `today_tasks`: INTEGER (count of tasks created or due today)
  - `category_breakdown`: ARRAY (counts of tasks per category)

- **Computed From**: Tasks table filtered by user_id with aggregations

## State Transitions

### Task State Transitions
- `created` → `active`: When task is initially saved
- `active` → `completed`: When user marks task as complete (via PATCH /api/tasks/{id}/complete)
- `completed` → `active`: When user unmarks task as complete (via PATCH /api/tasks/{id}/complete)

### Category Lifecycle
- `created` → `active`: When category is initially saved
- `active` → `deleted`: When category is removed (deletion behavior: reassign tasks or prevent deletion if tasks exist)

## Data Constraints

### Referential Integrity
- All foreign key constraints enforced at database level
- CASCADE delete for user deletion (deletes associated tasks and categories)
- RESTRICT delete for category if tasks still reference it (require reassignment first)

### Data Validation
- Length constraints enforced at database level
- NOT NULL constraints where required
- CHECK constraints for specific validation rules
- Unique constraints where appropriate

### Indexes for Performance
- Tasks table: INDEX on (user_id, completed) for efficient filtering
- Tasks table: INDEX on (user_id, category_id) for category-based queries
- Categories table: INDEX on (user_id) for user-based queries
- Tasks table: INDEX on (created_at) for chronological sorting

## Default Categories
When a new user registers, create these default categories:
1. Work (💼)
2. Personal (🏠)
3. Shopping (🛒)
4. Health (💪)
5. Learning (🎓)

## Security Considerations
- All queries must filter by user_id to enforce data isolation
- Category operations require user authentication and authorization
- Cross-user data access prevented by user_id constraints