"""
Dashboard statistics endpoints for the Todo API
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from sqlmodel import Session, select, func
from pydantic import BaseModel
from datetime import datetime, date, timedelta, timezone
from db import get_session
from models import Task, Category
from auth import get_current_user, verify_user_access, log_user_access_attempt

router = APIRouter(prefix="/api")

# Pydantic models for request/response
class TaskStatsResponse(BaseModel):
    total: int
    completed: int
    pending: int

class CategoryStatsResponse(BaseModel):
    category_id: int
    name: str
    icon: str
    count: int

class TodayTaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    category_id: Optional[int]
    due_time: Optional[str]
    created_at: datetime
    updated_at: datetime

class TodayTasksResponse(BaseModel):
    tasks: List[TodayTaskResponse]
    count: int

# GET /api/tasks/stats - Get task counts (total, completed, pending)
@router.get("/tasks/stats", response_model=TaskStatsResponse)
async def get_task_statistics(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get aggregated statistics about user's tasks (total, completed, pending)
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"GET /api/tasks/stats")

    # Count total tasks for the user
    total_query = select(func.count(Task.id)).where(Task.user_id == user_id)
    total = session.exec(total_query).one()

    # Count completed tasks for the user
    completed_query = select(func.count(Task.id)).where(
        Task.user_id == user_id,
        Task.completed == True
    )
    completed = session.exec(completed_query).one()

    # Calculate pending tasks
    pending = total - completed

    return TaskStatsResponse(
        total=total,
        completed=completed,
        pending=pending
    )


# GET /api/tasks/stats/categories - Get task count per category
@router.get("/tasks/stats/categories", response_model=List[CategoryStatsResponse])
async def get_category_statistics(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get task count per category for the authenticated user
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"GET /api/tasks/stats/categories")

    # Get all categories for the user with their task counts
    stmt = (
        select(Category.id, Category.name, Category.icon, func.count(Task.id).label('count'))
        .select_from(Category)
        .outerjoin(Task, (Task.category_id == Category.id) & (Task.user_id == user_id))
        .where(Category.user_id == user_id)
        .group_by(Category.id, Category.name, Category.icon)
        .order_by(func.count(Task.id).desc())
    )

    results = session.exec(stmt).all()

    category_stats = []
    for result in results:
        category_stats.append(
            CategoryStatsResponse(
                category_id=result.id,
                name=result.name,
                icon=result.icon,
                count=result.count
            )
        )

    return category_stats


# GET /api/tasks/today - Get tasks created or due today
@router.get("/tasks/today", response_model=TodayTasksResponse)
async def get_today_tasks(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: Optional[int] = 5
):
    """
    Get tasks created or due today for the authenticated user
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"GET /api/tasks/today")

    # Validate limit
    if limit is None:
        limit = 5
    elif limit < 1 or limit > 50:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit must be between 1 and 50"
        )

    # Get today's date boundaries in UTC to ensure consistency across timezones
    # Use UTC midnight as the start of "today" and 24 hours later as the end
    now_utc = datetime.now(timezone.utc)
    today_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # Query tasks created today (within the UTC day boundaries)
    # Using >= and < for proper range comparison
    stmt = (
        select(Task)
        .where(Task.user_id == user_id)
        .where(Task.created_at >= today_start.replace(tzinfo=None))  # Remove tzinfo for naive datetime comparison
        .where(Task.created_at < today_end.replace(tzinfo=None))
        .order_by(Task.created_at.desc())
        .limit(limit)
    )

    tasks = session.exec(stmt).all()

    # Convert to response format
    today_tasks = [
        TodayTaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            category_id=task.category_id,
            due_time=None,  # No due_time field in current model
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        for task in tasks
    ]

    return TodayTasksResponse(
        tasks=today_tasks,
        count=len(today_tasks)
    )