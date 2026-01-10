# Backend Development Environment - CLAUDE Documentation

## Project Overview
This is the backend component of the Todo Full-Stack Web Application, built with FastAPI and Python. It provides REST API endpoints for the application.

## Technology Stack
- **Backend Framework**: FastAPI 0.100+ (Modern Python API framework with automatic docs)
- **Backend Language**: Python 3.11+ (Performance, type hints, async support)
- **ORM**: SQLModel (Type-safe database operations with Pydantic)
- **Database**: Neon PostgreSQL (Serverless, scalable, reliable PostgreSQL)
- **Authentication**: JWT-based authentication with PyJWT

## Project Structure
```
backend-app/
├── main.py              # Application initialization, CORS, middleware
├── models.py            # SQLModel database model definitions
├── routes/              # Feature-based route handlers (setup.py, etc.)
├── db.py               # Database connection and session management
├── auth.py             # JWT verification and user extraction
├── config.py           # Configuration and environment variables
├── CLAUDE.md           # This documentation file
└── requirements.txt    # Dependency specifications
```

## Backend Principles (from Constitution)
- **File Organization**: One concern per file, feature-based route organization in `/routes`
- **Dependency Injection**: For shared logic
- **Middleware**: For cross-cutting concerns (auth, logging, CORS)

## API Conventions
- **URL Structure**: `/api/{user_id}/{resource}` for collections, `/api/{user_id}/{resource}/{id}` for specific items
- **HTTP Methods**: Standard REST conventions (GET, POST, PUT, PATCH, DELETE)
- **Status Codes**: Standard HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- **Response Format**: Always return JSON (except 204 No Content)
- **Field Naming**: Consistent snake_case for JSON responses
- **Authorization**: All requests must include Authorization header: `Authorization: Bearer <token>`

## Authentication & Security
- **JWT Authentication**: All API requests must be authenticated with JWT tokens
- **User Isolation**: ALL database queries MUST filter by authenticated user_id
- **Token Verification**: Backend must verify JWT signature using shared secret
- **Input Validation**: Use Pydantic models for request validation
- **Secrets Management**: Environment variables for ALL secrets, `.env` files in `.gitignore`

## Database Operations
- **SQLModel ORM**: ALL database access must go through SQLModel ORM
- **Connection Management**: Use dependency injection pattern with `get_session()`
- **User Data Isolation**: ALWAYS filter by user_id for user data
- **Schema Design**: Follow naming conventions (lowercase table names, snake_case columns)

## Development Workflow
1. **Setup**: Install dependencies with `uv sync`
2. **Environment**: Copy `.env.example` to `.env` and configure variables
3. **Run Development Server**: `uv run uvicorn main:app --reload --port 8000`
4. **API Documentation**: Available at `http://localhost:8000/docs`

## Required Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost:5432/backend_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-32-chars-min
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
PORT=8000
```

## Running the Application
```bash
# Run the development server with auto-reload
uv run uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000` with interactive API documentation at `http://localhost:8000/docs`.