from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import threading
import time
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

# Import MCP server components for AI Agent integration
from mcp.server import FastMCP
from task_mcp.tools.task_tools import (
    add_task as task_add_tool,
    list_tasks as task_list_tool,
    complete_task as task_complete_tool,
    delete_task as task_delete_tool,
    delete_task as task_delete_tool,
    update_task as task_update_tool,
    add_category as category_add_tool,
    list_categories as category_list_tool,
    delete_category as category_delete_tool
)
from pydantic import BaseModel, Field
from jose import jwt, JWTError
from fastapi import HTTPException, Header
from typing import Optional, Dict, Any
import json
from datetime import datetime

# MCP server thread reference
mcp_thread = None


def run_mcp_server_background():
    """Run MCP server in background thread"""
    import uvicorn
    mcp_app = mcp.streamable_http_app()
    mcp_port = int(os.getenv("MCP_PORT", 8808))
    print(f"[MCP] Starting MCP server on port {mcp_port}...")
    uvicorn.run(mcp_app, host="0.0.0.0", port=mcp_port, log_level="warning")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global mcp_thread
    
    # Create database tables on startup
    create_db_and_tables()
    
    # Start MCP server in background thread ONLY if not disabled
    # In Kubernetes, we run MCP as a separate service, so we can disable the embedded one
    if os.getenv("DISABLE_EMBEDDED_MCP", "false").lower() != "true":
        mcp_thread = threading.Thread(target=run_mcp_server_background, daemon=True)
        mcp_thread.start()
        print("[MCP] Background MCP server thread started")
    else:
        print("[MCP] Embedded MCP server disabled (running in distributed mode)")
    
    # Give MCP server time to start
    time.sleep(1)
    
    yield
    
    # Cleanup on shutdown
    print("[MCP] Shutting down...")


# Create FastAPI app instance
app = FastAPI(
    title="Todo API - Backend Development Environment",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiting middleware
app.add_middleware(APIRateLimitMiddleware)

# Configure CORS middleware (Must be adding LAST to be the OUTERMOST middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Auth is handled via dependency injection in routes (get_current_user)

# Include setup, task, dashboard, category, and chat routes
app.include_router(setup_router)
app.include_router(tasks_router)
app.include_router(dashboard_router)
app.include_router(categories_router)
app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Todo API Backend is running!"}


@app.get("/health")
async def health_check():
    """Health check endpoint - returns the health status of the backend service"""
    return {
        "status": "healthy",
        "timestamp": "2026-01-07T08:00:00Z"
    }


# Create MCP server instance for AI Agent tools
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
    category_id: Optional[int] = None
) -> dict:
    """Create a new task. Requires user_id, title. Optional: description, category_id."""
    return task_add_tool(user_id, title, description, category_id)


@mcp.tool(
    name="list_tasks",
    description="Retrieve tasks with optional filtering by status"
)
def list_tasks_wrapper(
    user_id: str,
    status: str = "all"
) -> list:
    """Get tasks. Requires user_id. Optional status: 'all', 'pending', 'completed'."""
    print(f"[MCP list_tasks] user_id={user_id}, status={status}")
    result = task_list_tool(user_id, status)
    print(f"[MCP list_tasks] result={result}")
    return result


@mcp.tool(
    name="complete_task",
    description="Mark a task as complete or incomplete"
)
def complete_task_wrapper(
    user_id: str,
    task_id: int
) -> dict:
    """Mark task as complete. Requires user_id and task_id."""
    return task_complete_tool(user_id, task_id)


@mcp.tool(
    name="delete_task",
    description="Remove a task from the database"
)
def delete_task_wrapper(
    user_id: str,
    task_id: int
) -> dict:
    """Delete a task. Requires user_id and task_id."""
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
    category_id: Optional[int] = None
) -> dict:
    """Update a task. Requires user_id, task_id. Optional: title, description, category_id."""
    return task_update_tool(user_id, task_id, title, description, category_id)


@mcp.tool(
    name="add_category",
    description="Create a new task category"
)
def add_category_wrapper(
    user_id: str,
    name: str,
    icon: str = "📁"
) -> dict:
    """Create a new category. Requires user_id, name. Optional: icon."""
    return category_add_tool(user_id, name, icon)


@mcp.tool(
    name="list_categories",
    description="Retrieve task categories"
)
def list_categories_wrapper(
    user_id: str
) -> list:
    """List categories. Requires user_id."""
    return category_list_tool(user_id)


@mcp.tool(
    name="delete_category",
    description="Delete a task category"
)
def delete_category_wrapper(
    user_id: str,
    category_id: int
) -> dict:
    """Delete a category. Requires user_id, category_id."""
    return category_delete_tool(user_id, category_id)


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """Health check tool for the MCP server"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Note: MCP server mount removed - AI agent now uses direct tool calls instead of HTTP


def run_mcp_server():
    """Function to run the MCP server in a separate thread"""
    print("MCP server functionality is available in the main application.")
    print("For production deployment, MCP server should be deployed separately.")
    print("For development, you can run 'python mcp_server.py' in a separate terminal.")

    # For now, just indicate that the MCP tools are available
    import time
    mcp_port = int(os.getenv("MCP_PORT", 8808))
    print(f"MCP tools are registered and available on port {mcp_port} (simulated)")

    # Keep the thread alive
    while True:
        time.sleep(60)


if __name__ == "__main__":
    import uvicorn
    import sys

    # Check if we should run both servers
    if len(sys.argv) > 1 and sys.argv[1] == "both":
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
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="info"
        )
    else:
        # Run only the main API server (default for Hugging Face deployment)
        print("Starting main API server...")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="info"
        )