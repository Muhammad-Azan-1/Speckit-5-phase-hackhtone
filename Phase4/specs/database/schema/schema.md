# Database Specification: Todo Application Schema

**Created**: 2026-01-07
**Status**: Draft
**Related Feature**: @specs/features/002-uv-fastapi-backend/spec.md

## Database Overview

This document specifies the database schema for the Todo application using PostgreSQL with SQLModel. The schema enforces data integrity, supports the application's requirements, and follows the naming conventions defined in the constitution.

## Database Configuration

- **Database Type**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel (Type-safe SQLAlchemy + Pydantic integration)
- **Connection**: Connection pooling with environment-based configuration
- **Naming Convention**: Lowercase table names, snake_case column names

## Schema Design Principles

1. **Data Integrity**: Enforced at the database level with constraints
2. **Performance**: Proper indexing for frequently queried columns
3. **Security**: User data isolation through user_id foreign keys
4. **Scalability**: Designed to handle growth in users and tasks

## Table Specifications

### 1. Users Table
- **Table Name**: `user` (Better Auth default)
- **Purpose**: Store user account information managed by Better Auth

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY, NOT NULL | User identifier from Better Auth |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| name | VARCHAR(255) | | User's display name |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Last update timestamp |

#### Indexes
- PRIMARY KEY: `id`
- UNIQUE: `email`

---

### 2. Tasks Table
- **Table Name**: `task`
- **Purpose**: Store individual todo tasks for users

#### Columns
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT, NOT NULL | Task identifier |
| title | VARCHAR(255) | NOT NULL, CHECK LENGTH(1-255) | Task title (1-255 characters) |
| description | TEXT | | Task description (optional, up to 1000 characters) |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| user_id | VARCHAR(255) | FOREIGN KEY, NOT NULL | Owner of the task |
| created_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Last update timestamp |

#### Indexes
- PRIMARY KEY: `id`
- FOREIGN KEY: `user_id` → `user.id`
- INDEX: `user_id` (for user-based queries)
- INDEX: `completed` (for status filtering)
- INDEX: `created_at` (for sorting)

#### Constraints
- `CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 255)`
- `CHECK (LENGTH(description) <= 1000)`
- Foreign key constraint ensures user_id references valid user

## Relationship Model

### User → Task (One-to-Many)
- One user can own many tasks
- Tasks are linked to users via `user_id` foreign key
- When a user is deleted, their tasks should be handled appropriately (to be defined)

### Data Isolation
- All queries must filter by `user_id` to enforce data isolation
- Users can only access tasks belonging to their `user_id`
- Backend API enforces this at the application level

## Security Requirements

1. **User Data Isolation**: All queries must include WHERE user_id = authenticated_user_id
2. **Foreign Key Constraints**: Enforce referential integrity
3. **Input Validation**: Column constraints enforce data quality at database level
4. **Audit Trail**: created_at and updated_at timestamps for all records

## Performance Considerations

### Indexing Strategy
- Primary keys automatically indexed
- Foreign keys indexed for join operations
- Frequently filtered columns indexed (completed status)
- Frequently sorted columns indexed (created_at)

### Query Optimization
- Use parameterized queries to prevent SQL injection
- Limit result sets with pagination (LIMIT/OFFSET)
- Use appropriate WHERE clauses to leverage indexes

## Migration Strategy

### Initial Schema Creation
- Use SQLModel's metadata.create_all() for initial setup
- Verify database connectivity before operations
- Handle migration scenarios for future schema changes

### Future Changes
- Use proper migration tools (Alembic) for production
- Maintain backward compatibility during schema changes
- Plan for zero-downtime deployments

## Environment Configuration

Database connection string follows the format:
```
postgresql://username:password@host:port/database_name
```

Configuration stored in environment variables:
- `DATABASE_URL` - Full connection string for Neon PostgreSQL

## API Integration Points

This schema supports the API endpoints defined in:
- `@specs/api/rest-endpoints.md`

The following API operations map to database operations:
- GET /api/{user_id}/tasks → SELECT from task WHERE user_id = ?
- POST /api/{user_id}/tasks → INSERT into task with user_id
- GET /api/{user_id}/tasks/{id} → SELECT from task WHERE user_id = ? AND id = ?
- PUT /api/{user_id}/tasks/{id} → UPDATE task SET ... WHERE user_id = ? AND id = ?
- DELETE /api/{user_id}/tasks/{id} → DELETE from task WHERE user_id = ? AND id = ?
- PATCH /api/{user_id}/tasks/{id}/complete → UPDATE task SET completed = ? WHERE user_id = ? AND id = ?