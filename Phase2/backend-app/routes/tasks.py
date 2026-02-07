"""
Task management endpoints for the Todo API
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import datetime
from db import get_session
from models import Task
from auth import get_current_user, verify_user_access, log_user_access_attempt

router = APIRouter(prefix="/api/{user_id}")

# Pydantic models for request/response
class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = None

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    category_id: Optional[int] = None
    version: Optional[int] = None  # For optimistic locking

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime

# POST /api/{user_id}/tasks - Create new task
@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_request: TaskCreateRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user
    """
    # Verify that the authenticated user matches the requested user_id
    verify_user_access(user_id, current_user)

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"POST /api/{user_id}/tasks")

    # Validate title length (1-255 characters as specified in requirements)
    if len(task_request.title) < 1 or len(task_request.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be between 1 and 255 characters"
        )

    # Validate description length (0-1000 characters as specified in requirements)
    if task_request.description is not None and len(task_request.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be between 0 and 1000 characters"
        )

    # Create new task
    new_task = Task(
        title=task_request.title,
        description=task_request.description,
        completed=False,  # Default to not completed
        user_id=user_id,
        category_id=task_request.category_id,
        version=1  # Initialize version for optimistic locking
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    # Get category name if category_id is set
    category_name = None
    if new_task.category_id:
        from models import Category
        category = session.exec(select(Category).where(Category.id == new_task.category_id)).first()
        if category:
            category_name = category.name

    return TaskResponse(
        id=new_task.id,
        title=new_task.title,
        description=new_task.description,
        completed=new_task.completed,
        user_id=new_task.user_id,
        category_id=new_task.category_id,
        category_name=category_name,
        version=new_task.version,
        created_at=new_task.created_at,
        updated_at=new_task.updated_at
    )


# GET /api/{user_id}/tasks - List all user tasks with filtering, sorting, pagination
@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    status_filter: Optional[str] = None,  # pending, completed, all
    sort: Optional[str] = "created",  # created, updated, title
    order: Optional[str] = "desc",  # asc, desc
    limit: Optional[int] = 50,  # 1-100
    offset: Optional[int] = 0
):
    """
    List all tasks for the specified user with support for filtering, sorting, and pagination
    """
    # Verify that the authenticated user matches the requested user_id
    verify_user_access(user_id, current_user)

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"GET /api/{user_id}/tasks")

    # Build query with user_id filter
    query = select(Task).where(Task.user_id == user_id)

    # Apply status filter if specified
    if status_filter and status_filter.lower() != "all":
        if status_filter.lower() == "completed":
            query = query.where(Task.completed == True)
        elif status_filter.lower() == "pending":
            query = query.where(Task.completed == False)

    # Apply sorting
    if sort == "created":
        if order == "desc":
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())
    elif sort == "updated":
        if order == "desc":
            query = query.order_by(Task.updated_at.desc())
        else:
            query = query.order_by(Task.updated_at.asc())
    elif sort == "title":
        if order == "desc":
            query = query.order_by(Task.title.desc())
        else:
            query = query.order_by(Task.title.asc())

    # Apply pagination
    query = query.offset(offset).limit(min(limit, 100))  # Cap limit at 100

    # Execute query
    tasks = session.exec(query).all()

    # Get all categories for this user to build category name map
    from models import Category
    categories_query = select(Category).where(Category.user_id == user_id)
    categories = session.exec(categories_query).all()
    category_map = {cat.id: cat.name for cat in categories}

    # Convert to response format
    task_responses = [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            category_id=task.category_id,
            category_name=category_map.get(task.category_id) if task.category_id else None,
            version=task.version,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]

    return task_responses


# GET /api/{user_id}/tasks/{id} - Get specific task details
@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get details for a specific task
    """
    # Verify that the authenticated user matches the requested user_id
    verify_user_access(user_id, current_user)

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"GET /api/{user_id}/tasks/{task_id}")

    # Find the task by ID and user_id
    task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Get category name if category_id is set
    category_name = None
    if task.category_id:
        from models import Category
        category = session.exec(select(Category).where(Category.id == task.category_id)).first()
        if category:
            category_name = category.name

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        category_id=task.category_id,
        category_name=category_name,
        version=task.version,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


# PUT /tasks/{task_id} - Update entire task (router prefix is /api/{user_id})
@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdateRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an entire task with new values
    """
    # Verify that the authenticated user matches the requested user_id
    verify_user_access(user_id, current_user)

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"PUT /api/{user_id}/tasks/{task_id}")

    # Find the task by ID and user_id
    task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check version for optimistic locking if provided
    if task_update.version is not None and task_update.version != task.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task was modified by another user. Please refresh and try again."
        )

    # Update fields if provided in the request
    if task_update.title is not None:
        # Validate title length (1-200 characters as per specification)
        if len(task_update.title) < 1 or len(task_update.title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be between 1 and 200 characters"
            )
        task.title = task_update.title

    if task_update.description is not None:
        # Validate description length (0-1000 characters)
        if len(task_update.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be between 0 and 1000 characters"
            )
        task.description = task_update.description

    if task_update.completed is not None:
        task.completed = task_update.completed

    if task_update.category_id is not None:
        task.category_id = task_update.category_id

    # Increment the version for optimistic locking
    task.version += 1
    # Update the updated_at timestamp
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Get category name if category_id is set
    category_name = None
    if task.category_id:
        from models import Category
        category = session.exec(select(Category).where(Category.id == task.category_id)).first()
        if category:
            category_name = category.name

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        category_id=task.category_id,
        category_name=category_name,
        version=task.version,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


# DELETE /api/{user_id}/tasks/{task_id} - Delete task permanently
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently
    """
    # Verify that the authenticated user matches the requested user_id
    verify_user_access(user_id, current_user)

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"DELETE /api/{user_id}/tasks/{task_id}")

    # Find the task by ID and user_id
    task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()


# PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle task completion status
@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task
    """
    # Verify that the authenticated user matches the requested user_id
    verify_user_access(user_id, current_user)

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"PATCH /api/{user_id}/tasks/{task_id}/complete")

    # Find the task by ID and user_id
    task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status
    task.completed = not task.completed
    # Increment the version for optimistic locking
    task.version += 1
    # Update the updated_at timestamp
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Get category name if category_id is set
    category_name = None
    if task.category_id:
        from models import Category
        category = session.exec(select(Category).where(Category.id == task.category_id)).first()
        if category:
            category_name = category.name

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        category_id=task.category_id,
        category_name=category_name,
        version=task.version,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


# PATCH /api/{user_id}/tasks/{task_id} - Update specific fields of a task (for optimistic locking)
@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task_fields(
    user_id: str,
    task_id: int,
    task_update: TaskUpdateRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update specific fields of a task with optimistic locking
    """
    # Verify that the authenticated user matches the requested user_id
    verify_user_access(user_id, current_user)

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"PATCH /api/{user_id}/tasks/{task_id}")

    # Find the task by ID and user_id
    task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Check version for optimistic locking if provided
    if task_update.version is not None and task_update.version != task.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task was modified by another user. Please refresh and try again."
        )

    # Update fields if provided in the request
    if task_update.title is not None:
        # Validate title length (1-200 characters as per specification)
        if len(task_update.title) < 1 or len(task_update.title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be between 1 and 200 characters"
            )
        task.title = task_update.title

    if task_update.description is not None:
        # Validate description length (0-1000 characters)
        if len(task_update.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be between 0 and 1000 characters"
            )
        task.description = task_update.description

    if task_update.completed is not None:
        task.completed = task_update.completed

    if task_update.category_id is not None:
        task.category_id = task_update.category_id

    # Increment the version for optimistic locking
    task.version += 1
    # Update the updated_at timestamp
    task.updated_at = datetime.now()

    session.add(task)
    session.commit()
    session.refresh(task)

    # Get category name if category_id is set
    category_name = None
    if task.category_id:
        from models import Category
        category = session.exec(select(Category).where(Category.id == task.category_id)).first()
        if category:
            category_name = category.name

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        category_id=task.category_id,
        category_name=category_name,
        version=task.version,
        created_at=task.created_at,
        updated_at=task.updated_at
    )