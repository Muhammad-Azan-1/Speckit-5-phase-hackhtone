"""
MCP Server for AI Chatbot Integration - Exposes tools for AI agents to interact with the task system
Based on the constitution specification for Phase 3 AI Chatbot integration
Simplified: Authentication is handled at the API level, not in MCP tools
"""
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Import the MCP SDK
from mcp.server import FastMCP

# Import task tools (the actual database operations)
from task_mcp.tools.task_tools import (
    add_task as task_add_tool,
    list_tasks as task_list_tool,
    complete_task as task_complete_tool,
    delete_task as task_delete_tool,
    delete_task as task_delete_tool,
    update_task as task_update_tool,
    add_category as category_add_tool,
    list_categories as category_list_tool
)

# Load environment variables
load_dotenv()

# Create an MCP server instance using FastMCP
mcp = FastMCP("Task Management MCP Server", json_response=True)


@mcp.tool(
    name="add_task",
    description="Create a new task in the database"
)
def add_task_wrapper(
    user_id: str,
    title: str,
    description: str = ""
) -> dict:
    """
    Create a new task for the specified user.
    
    Args:
        user_id: The user ID who owns this task
        title: The task title (required)
        description: Optional task description
    
    Returns:
        Dictionary with task_id, status, and title
    """
    return task_add_tool(user_id, title, description)


@mcp.tool(
    name="list_tasks",
    description="Retrieve tasks with optional filtering by status"
)
def list_tasks_wrapper(
    user_id: str,
    status: str = "all"
) -> list:
    """
    List tasks for the specified user.
    
    Args:
        user_id: The user ID to list tasks for
        status: Filter - "all", "pending", or "completed" (default: "all")
    
    Returns:
        List of task dictionaries
    """
    return task_list_tool(user_id, status)


@mcp.tool(
    name="complete_task",
    description="Mark a task as complete or incomplete"
)
def complete_task_wrapper(
    user_id: str,
    task_id: int
) -> dict:
    """
    Toggle task completion status.
    
    Args:
        user_id: The user ID who owns this task
        task_id: The ID of the task to complete
    
    Returns:
        Dictionary with task_id, status, and title
    """
    return task_complete_tool(user_id, task_id)


@mcp.tool(
    name="delete_task",
    description="Remove a task from the database"
)
def delete_task_wrapper(
    user_id: str,
    task_id: int
) -> dict:
    """
    Delete a task permanently.
    
    Args:
        user_id: The user ID who owns this task
        task_id: The ID of the task to delete
    
    Returns:
        Dictionary with task_id, status, and title
    """
    return task_delete_tool(user_id, task_id)


@mcp.tool(
    name="update_task",
    description="Modify task title, description, or category"
)
def update_task_wrapper(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update an existing task.
    
    Args:
        user_id: The user ID who owns this task
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
    
    Returns:
        Dictionary with task_id, status, and title
    """
    return task_update_tool(user_id, task_id, title, description)


@mcp.tool(
    name="add_category",
    description="Create a new task category"
)
def add_category_wrapper(
    user_id: str,
    name: str,
    icon: str = "📁"
) -> dict:
    """
    Create a new category for organizing tasks.
    
    Args:
        user_id: The user ID who owns this category
        name: The category name
        icon: Optional emoji icon (default: "📁")
    
    Returns:
        Dictionary with category details
    """
    return category_add_tool(user_id, name, icon)


@mcp.tool(
    name="list_categories",
    description="Retrieve task categories"
)
def list_categories_wrapper(
    user_id: str
) -> list:
    """
    List categories for the specified user.
    
    Args:
        user_id: The user ID to list categories for
    
    Returns:
        List of category dictionaries
    """
    return category_list_tool(user_id)


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """Health check tool for the MCP server"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# Run the server with streamable HTTP transport
if __name__ == "__main__":
    import uvicorn
    
    # Create the MCP server app
    mcp_app = mcp.streamable_http_app()
    
    # Run on MCP_PORT (default 8808)
    mcp_port = int(os.getenv("MCP_PORT", 8808))
    print(f"Starting MCP server on port {mcp_port}")
    uvicorn.run(mcp_app, host="0.0.0.0", port=mcp_port)