# Quickstart Guide: Todo API Endpoints

## Prerequisites

- Python 3.11+
- uv package manager installed
- Access to Neon PostgreSQL (or local PostgreSQL for development)

## Setup Steps

### 1. Initialize the Project

```bash
# Install uv if not already installed
pip install uv

# Navigate to the backend directory
cd backend-app
```

### 2. Install Dependencies

```bash
# Add FastAPI with standard dependencies
uv add "fastapi[standard]"

# Add SQLModel for database operations
uv add sqlmodel

# Add database driver (for PostgreSQL)
uv add psycopg2-binary

# Add JWT library for authentication
uv add "PyJWT[crypto]>=2.0.0"
```

### 3. Create the Basic Project Structure

Create the following files based on the constitution's required structure:

```
backend-app/
├── main.py              # Application initialization
├── models.py            # SQLModel database models
├── db.py               # Database connection and session management
├── auth.py             # JWT verification and user extraction
├── routes/             # Feature-based route handlers
│   └── tasks.py        # Task-related endpoints
└── config.py           # Configuration and environment variables
```

### 4. Environment Configuration

Create a `.env` file with the required environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-32-chars-min
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
```

### 5. Run the Backend

```bash
# Run the development server with auto-reload
uv run uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000` with interactive API documentation at `http://localhost:8000/docs`.

## API Usage Examples

### Create a Task
```bash
curl -X POST http://localhost:8000/api/user123/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Need to buy milk, eggs, and bread"}'
```

### Get User's Tasks
```bash
curl -X GET "http://localhost:8000/api/user123/tasks?limit=10&offset=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/api/user123/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated task title", "description": "Updated description", "completed": true}'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/api/user123/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Toggle Task Completion
```bash
curl -X PATCH http://localhost:8000/api/user123/tasks/1/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Next Steps

1. Implement the required API endpoints as specified in the constitution
2. Create database models for the Task entity
3. Implement authentication middleware
4. Add your business logic to the routes