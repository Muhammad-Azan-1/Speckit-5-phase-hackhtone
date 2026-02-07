"""
MCP Tools for Task Operations - Implements the 5 required task operations for AI agent integration
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from models import Task as TaskModel
from db import engine  # Import engine directly instead of get_session
from datetime import datetime
import os
from jose import jwt, JWTError
from fastapi import HTTPException, Header


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


def add_task(user_id: str, title: str, description: str = "", category_id: Optional[int] = None) -> dict:
    """
    Create a new task in database.

    Args:
        user_id: The authenticated user's ID from JWT token
        title: The task title (required)
        description: Optional task description
        category_id: Optional category ID to associate with task

    Returns:
        Dictionary with task_id, status, and title
    """
    with Session(engine) as session:
        try:
            # Create new task
            task = TaskModel(
                title=title,
                description=description if description else None,
                completed=False,
                user_id=user_id,
                category_id=category_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "category_id": task.category_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        except Exception as e:
            session.rollback()
            return {"error": f"Error creating task: {str(e)}"}


def list_tasks(user_id: str, status: str = "all") -> list:
    """
    Retrieve tasks filtered by status.

    Args:
        user_id: The authenticated user's ID from JWT token
        status: Filter status - "all", "pending", or "completed" (default: "all")

    Returns:
        List of task dictionaries with id, title, completed status, and optional category
    """
    with Session(engine) as session:
        try:
            # Build query with user_id filter
            query = select(TaskModel).where(TaskModel.user_id == user_id)

            # Apply status filter
            if status == "pending":
                query = query.where(TaskModel.completed == False)
            elif status == "completed":
                query = query.where(TaskModel.completed == True)
            # For "all", no additional filter needed

            # Execute query
            tasks = session.exec(query.order_by(TaskModel.created_at.desc())).all()

            # Convert to dictionaries
            tasks_list = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                }

                # Add category information if available
                if task.category_id:
                    # In a real implementation, we'd join with the Category table
                    # For now, we'll just include the category_id
                    task_dict["category_id"] = task.category_id

                tasks_list.append(task_dict)

            return tasks_list
        except Exception as e:
            return [{"error": f"Error listing tasks: {str(e)}"}]



def complete_task(user_id: str, task_id: int) -> dict:
    """
    Toggle task completion status in database.

    Args:
        user_id: The authenticated user's ID from JWT token
        task_id: The ID of the task to update

    Returns:
        Dictionary with full task details
    """
    with Session(engine) as session:
        try:
            # Find the task for the current user
            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {"error": "Task not found or access denied"}

            # Update task completion status
            task.completed = not task.completed  # Toggle completion status
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "category_id": task.category_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        except Exception as e:
            session.rollback()
            return {"error": f"Error updating task: {str(e)}"}
            

def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    category_id: Optional[int] = None
) -> dict:
    """
    Modify task title, description or category.

    Args:
        user_id: The authenticated user's ID from JWT token
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        category_id: New category ID (optional)

    Returns:
        Dictionary with full task details
    """
    with Session(engine) as session:
        try:
            # Find the task for the current user
            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {"error": "Task not found or access denied"}

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if category_id is not None:
                task.category_id = category_id

            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "category_id": task.category_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        except Exception as e:
            session.rollback()
            return {"error": f"Error updating task: {str(e)}"}



def add_category(user_id: str, name: str, icon: str = "📁") -> dict:
    """
    Create a new category in database.

    Args:
        user_id: The authenticated user's ID from JWT token
        name: The category name (required)
        icon: Optional emoji icon (default: "📁")

    Returns:
        Dictionary with category_id, name, and icon
    """
    from models import Category as CategoryModel  # Import locally to avoid circular imports

    with Session(engine) as session:
        try:
            # Create new category
            category = CategoryModel(
                name=name,
                icon=icon,
                user_id=user_id,
                created_at=datetime.utcnow()
            )

            session.add(category)
            session.commit()
            session.refresh(category)

            return {
                "id": category.id,
                "name": category.name,
                "icon": category.icon,
                "user_id": category.user_id,
                "created_at": category.created_at.isoformat()
            }
        except Exception as e:
            session.rollback()
            return {"error": f"Error creating category: {str(e)}"}


def list_categories(user_id: str) -> list:
    """
    Retrieve categories for a user.

    Args:
        user_id: The authenticated user's ID from JWT token

    Returns:
        List of category dictionaries
    """
    from models import Category as CategoryModel

    with Session(engine) as session:
        try:
            # Build query with user_id filter
            query = select(CategoryModel).where(CategoryModel.user_id == user_id)
            
            # Execute query
            categories = session.exec(query.order_by(CategoryModel.created_at.desc())).all()

            # Convert to dictionaries
            categories_list = []
            for category in categories:
                categories_list.append({
                    "id": category.id,
                    "name": category.name,
                    "icon": category.icon
                })

            return categories_list
        except Exception as e:
            return [{"error": f"Error listing categories: {str(e)}"}]



def delete_category(user_id: str, category_id: int) -> dict:
    """
    Remove category from database. Tasks in this category will become uncategorized.

    Args:
        user_id: The authenticated user's ID from JWT token
        category_id: The ID of the category to delete

    Returns:
        Dictionary with category_id and status
    """
    from models import Category as CategoryModel

    with Session(engine) as session:
        try:
            # Find the category by ID and user_id
            category = session.exec(
                select(CategoryModel)
                .where(CategoryModel.id == category_id)
                .where(CategoryModel.user_id == user_id)
            ).first()

            if not category:
                return {"error": "Category not found"}

            # Orphan any tasks associated with this category (set category_id to NULL)
            # Tasks will remain but become uncategorized
            orphan_stmt = select(TaskModel).where(TaskModel.category_id == category_id).where(TaskModel.user_id == user_id)
            associated_tasks = session.exec(orphan_stmt).all()
            for task in associated_tasks:
                task.category_id = None
                session.add(task)

            session.delete(category)
            session.commit()

            return {
                "category_id": category_id,
                "status": "deleted",
                "message": "Category deleted, tasks moved to uncategorized"
            }
        except Exception as e:
            session.rollback()
            return {"error": f"Error deleting category: {str(e)}"}


def delete_task(user_id: str, task_id: int) -> dict:
    """
    Remove task from database.

    Args:
        user_id: The authenticated user's ID from JWT token
        task_id: The ID of the task to delete

    Returns:
        Dictionary with task_id, status, and title
    """
    with Session(engine) as session:
        try:
            # Find the task for the current user
            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {"error": "Task not found or access denied"}

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                "task_id": task.id,
                "status": "deleted",
                "title": task.title
            }
        except Exception as e:
            session.rollback()
            return {"error": f"Error deleting task: {str(e)}"}


def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    category_id: Optional[int] = None
) -> dict:
    """
    Modify task title, description or category.

    Args:
        user_id: The authenticated user's ID from JWT token
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        category_id: New category ID (optional)

    Returns:
        Dictionary with task_id, status, and title
    """
    with Session(engine) as session:
        try:
            # Find the task for the current user
            statement = select(TaskModel).where(
                TaskModel.id == task_id,
                TaskModel.user_id == user_id
            )
            task = session.exec(statement).first()

            if not task:
                return {"error": "Task not found or access denied"}

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if category_id is not None:
                task.category_id = category_id

            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
        except Exception as e:
            session.rollback()
            return {"error": f"Error updating task: {str(e)}"}