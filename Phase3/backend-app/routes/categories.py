"""
Category management endpoints for the Todo API
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import datetime
from db import get_session
from models import Category, Task
from auth import get_current_user, verify_user_access, log_user_access_attempt

router = APIRouter(prefix="/api")

# Pydantic models for request/response
class CategoryCreateRequest(BaseModel):
    name: str
    icon: str

class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    icon: str
    user_id: str
    created_at: datetime

# GET /api/categories - Get all user's categories
@router.get("/categories", response_model=list[CategoryResponse])
async def get_categories(
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all categories for the authenticated user
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"GET /api/categories")

    # Get all categories for the user
    stmt = select(Category).where(Category.user_id == user_id).order_by(Category.created_at.desc())
    categories = session.exec(stmt).all()

    return [
        CategoryResponse(
            id=category.id,
            name=category.name,
            icon=category.icon,
            user_id=category.user_id,
            created_at=category.created_at
        )
        for category in categories
    ]


# POST /api/categories - Create new category
@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_request: CategoryCreateRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new category for the authenticated user
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"POST /api/categories")

    # Validate name length (1-50 characters)
    if len(category_request.name) < 1 or len(category_request.name) > 50:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Category name must be between 1 and 50 characters"
        )

    # Validate icon length (1-10 characters)
    if len(category_request.icon) < 1 or len(category_request.icon) > 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Category icon must be between 1 and 10 characters"
        )

    # Create new category
    new_category = Category(
        name=category_request.name,
        icon=category_request.icon,
        user_id=user_id
    )

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return CategoryResponse(
        id=new_category.id,
        name=new_category.name,
        icon=new_category.icon,
        user_id=new_category.user_id,
        created_at=new_category.created_at
    )


# GET /api/categories/{id} - Get specific category details
@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get details of a specific category
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"GET /api/categories/{category_id}")

    # Find the category by ID and user_id
    category = session.exec(
        select(Category)
        .where(Category.id == category_id)
        .where(Category.user_id == user_id)
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return CategoryResponse(
        id=category.id,
        name=category.name,
        icon=category.icon,
        user_id=category.user_id,
        created_at=category.created_at
    )


# PUT /api/categories/{id} - Update category
@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdateRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing category for the authenticated user
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"PUT /api/categories/{category_id}")

    # Find the category by ID and user_id
    category = session.exec(
        select(Category)
        .where(Category.id == category_id)
        .where(Category.user_id == user_id)
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Update fields if provided in the request
    if category_update.name is not None:
        # Validate name length (1-50 characters)
        if len(category_update.name) < 1 or len(category_update.name) > 50:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Category name must be between 1 and 50 characters"
            )
        category.name = category_update.name

    if category_update.icon is not None:
        # Validate icon length (1-10 characters)
        if len(category_update.icon) < 1 or len(category_update.icon) > 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Category icon must be between 1 and 10 characters"
            )
        category.icon = category_update.icon

    session.add(category)
    session.commit()
    session.refresh(category)

    return CategoryResponse(
        id=category.id,
        name=category.name,
        icon=category.icon,
        user_id=category.user_id,
        created_at=category.created_at
    )


# DELETE /api/categories/{id} - Delete category
@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a category permanently
    """
    user_id = current_user

    # Log the access attempt
    log_user_access_attempt(user_id, current_user, f"DELETE /api/categories/{category_id}")

    # Find the category by ID and user_id
    category = session.exec(
        select(Category)
        .where(Category.id == category_id)
        .where(Category.user_id == user_id)
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Orphan any tasks associated with this category (set category_id to NULL)
    # Tasks will remain but become uncategorized
    orphan_stmt = select(Task).where(Task.category_id == category_id).where(Task.user_id == user_id)
    associated_tasks = session.exec(orphan_stmt).all()
    for task in associated_tasks:
        task.category_id = None
        session.add(task)

    session.delete(category)
    session.commit()