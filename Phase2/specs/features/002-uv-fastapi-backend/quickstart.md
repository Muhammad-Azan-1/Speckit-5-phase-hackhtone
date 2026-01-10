# Quickstart Guide: Backend Development Environment Setup

## Prerequisites

- Python 3.11+
- uv package manager installed
- Access to Neon PostgreSQL (or local PostgreSQL for development)

## Setup Steps

### 1. Initialize the Project

```bash
# Install uv if not already installed
pip install uv

# Initialize a new Python project
uv init --package ./backend-app

# Navigate to the project directory
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

# Add Better Auth for authentication
uv add better-auth
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
│   └── setup.py        # Setup-related endpoints
└── config.py           # Configuration and environment variables
```

### 4. Environment Configuration

Create a `.env` file with the required environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/backend_db
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

## Next Steps

1. Implement the required API endpoints as specified in the constitution
2. Create database models for your specific application needs
3. Implement authentication middleware
4. Add your business logic to the routes