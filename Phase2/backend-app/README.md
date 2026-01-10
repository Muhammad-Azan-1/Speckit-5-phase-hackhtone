---
title: Todo App Backend
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Backend Development Environment API

This is a backend development environment API built with FastAPI and Python. It provides tools and endpoints for initializing and managing backend projects.

## Features

- Project initialization with proper structure and dependencies
- FastAPI-based REST API
- JWT-based authentication
- SQLModel for database operations
- Environment configuration management

## Tech Stack

- Python 3.11+
- FastAPI 0.100+
- uv for package management
- SQLModel for database operations
- Neon PostgreSQL
- JWT for authentication

## Deployment to Hugging Face Spaces

This backend is configured for deployment on Hugging Face Spaces using Docker.

For detailed, step-by-step deployment instructions, please read [README_DEPLOY.md](./README_DEPLOY.md).

## Setup and Installation

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv sync
   ```
3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
4. Update the .env file with your configuration
5. Run the development server:
   ```bash
   uv run uvicorn main:app --reload --port 8000
   ```

## Running the Application

To run the development server with auto-reload:

```bash
uv run uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000` with interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

- `GET /` - Root endpoint returning API status
- `GET /health` - Health check endpoint
- `POST /api/{user_id}/setup` - Initialize backend project

## Environment Configuration

Create a `.env` file with the required variables as documented in `.env.example`.

## Development

This project follows the layered architecture pattern with:
- Presentation Layer (handled by FastAPI)
- Application Layer (business logic in routes, services)
- Data Layer (SQLModel models and database operations)

## Security

- JWT-based authentication for all protected endpoints
- User data isolation enforced at all levels
- Input validation using Pydantic models
- Secrets management through environment variables