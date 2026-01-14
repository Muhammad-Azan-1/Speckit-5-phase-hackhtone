"""
Unified Server for Production Deployment
Combines FastAPI backend with MCP server for deployment on Hugging Face
"""
import os
import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.setup import router as setup_router
from routes.tasks import router as tasks_router
from routes.dashboard import router as dashboard_router
from routes.categories import router as categories_router
from routes.user import router as user_router
from routes.chat import router as chat_router
from db import create_db_and_tables
from contextlib import asynccontextmanager
from rate_limit_general import APIRateLimitMiddleware

# Load environment variables
load_dotenv()

# Import MCP server components
from mcp.server import FastMCP
from task_mcp.tools.task_tools import (
    add_task as task_add_tool,
    list_tasks as task_list_tool,
    complete_task as task_complete_tool,
    delete_task as task_delete_tool,
    update_task as task_update_tool
)
from pydantic import BaseModel, Field
from jose import jwt, JWTError
from fastapi import HTTPException, Header
from typing import Optional, Dict, Any
import json
from datetime import datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown if needed


# Create main FastAPI app instance
main_app = FastAPI(
    title="Todo API - Backend Development Environment",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiting middleware
main_app.add_middleware(APIRateLimitMiddleware)

# Configure CORS middleware (Must be adding LAST to be the OUTERMOST middleware)
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include setup, task, dashboard, category, and chat routes
main_app.include_router(setup_router)
main_app.include_router(tasks_router)
main_app.include_router(dashboard_router)
main_app.include_router(categories_router)
main_app.include_router(user_router)
main_app.include_router(chat_router)


@main_app.get("/")
async def root():
    return {"message": "Todo API Backend is running!"}


@main_app.get("/health")
async def health_check():
    """Health check endpoint - returns the health status of the backend service"""
    return {
        "status": "healthy",
        "timestamp": "2026-01-07T08:00:00Z"
    }


# Create MCP server instance
mcp = FastMCP("Task Management MCP Server", json_response=True)


class TaskSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(False, description="Task completion status")
    user_id: str = Field(..., description="User ID associated with the task")
    category_id: Optional[int] = Field(None, description="Associated category ID")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")


def verify_jwt_token(authorization: str = Header(None)):
    """
    Verify JWT token from Authorization header to get current user
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization[7:]  # Remove "Bearer " prefix

    try:
        SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
        ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            return None

        return user_id
    except JWTError:
        return None


@mcp.tool(
    name="add_task",
    description="Create a new task in the database"
)
def add_task_wrapper(
    user_id: str,
    title: str,
    description: str = "",
    category_id: Optional[int] = None,
    authorization: Optional[str] = None
) -> dict:
    """
    Wrapper for the add_task tool to match the specification.
    """
    # Verify the user from authorization header
    current_user_id = verify_jwt_token(authorization)

    if not current_user_id or current_user_id != user_id:
        return {"error": "Unauthorized: Invalid or missing token or user mismatch"}

    return task_add_tool(user_id, title, description, category_id)


@mcp.tool(
    name="list_tasks",
    description="Retrieve tasks with optional filtering by status"
)
def list_tasks_wrapper(
    user_id: str,
    status: str = "all",
    authorization: Optional[str] = None
) -> list:
    """
    Wrapper for the list_tasks tool to match the specification.
    """
    # Verify the user from authorization header
    current_user_id = verify_jwt_token(authorization)

    if not current_user_id or current_user_id != user_id:
        return [{"error": "Unauthorized: Invalid or missing token or user mismatch"}]

    return task_list_tool(user_id, status)


@mcp.tool(
    name="complete_task",
    description="Mark a task as complete or incomplete"
)
def complete_task_wrapper(
    user_id: str,
    task_id: int,
    authorization: Optional[str] = None
) -> dict:
    """
    Wrapper for the complete_task tool to match the specification.
    """
    # Verify the user from authorization header
    current_user_id = verify_jwt_token(authorization)

    if not current_user_id or current_user_id != user_id:
        return {"error": "Unauthorized: Invalid or missing token or user mismatch"}

    return task_complete_tool(user_id, task_id)


@mcp.tool(
    name="delete_task",
    description="Remove a task from the database"
)
def delete_task_wrapper(
    user_id: str,
    task_id: int,
    authorization: Optional[str] = None
) -> dict:
    """
    Wrapper for the delete_task tool to match the specification.
    """
    # Verify the user from authorization header
    current_user_id = verify_jwt_token(authorization)

    if not current_user_id or current_user_id != user_id:
        return {"error": "Unauthorized: Invalid or missing token or user mismatch"}

    return task_delete_tool(user_id, task_id)


@mcp.tool(
    name="update_task",
    description="Modify task title, description, or category"
)
def update_task_wrapper(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    category_id: Optional[int] = None,
    authorization: Optional[str] = None
) -> dict:
    """
    Wrapper for the update_task tool to match the specification.
    """
    # Verify the user from authorization header
    current_user_id = verify_jwt_token(authorization)

    if not current_user_id or current_user_id != user_id:
        return {"error": "Unauthorized: Invalid or missing token or user mismatch"}

    return task_update_tool(user_id, task_id, title, description, category_id)


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """Health check tool for the MCP server"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


def run_mcp_server():
    """Function to run the MCP server in a separate thread"""
    import uvicorn

    # Create the MCP server app using the streamable HTTP transport
    mcp_app = mcp.streamable_http_app()

    # Run on MCP port (different from main API port)
    mcp_port = int(os.getenv("MCP_PORT", 8808))
    print(f"Starting MCP server on port {mcp_port}")

    uvicorn.run(mcp_app, host="0.0.0.0", port=mcp_port)


if __name__ == "__main__":
    import uvicorn
    import sys

    # Determine which server to run based on command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        # Run only the MCP server
        run_mcp_server()
    elif len(sys.argv) > 1 and sys.argv[1] == "both":
        # Run both servers - MCP in a separate thread and main API in main thread
        mcp_thread = threading.Thread(target=run_mcp_server, daemon=True)
        mcp_thread.start()

        # Give the MCP server a moment to start
        time.sleep(2)

        print("Both servers starting...")
        print(f"MCP server running on port {os.getenv('MCP_PORT', 8808)}")
        print(f"Main API server running on port {os.getenv('PORT', 8000)}")

        # Run the main API server
        uvicorn.run(
            main_app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="info"
        )
    else:
        # Run only the main API server (default)
        uvicorn.run(
            main_app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="info"
        )