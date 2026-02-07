"""
Service module for category-related operations
"""
from sqlmodel import Session, select
from models import Category, Task
from datetime import datetime


def validate_category_before_deletion(session: Session, category_id: int, user_id: str) -> dict:
    """
    Validate if a category can be deleted and return validation result
    """
    # Check if category exists and belongs to user
    category = session.exec(
        select(Category)
        .where(Category.id == category_id)
        .where(Category.user_id == user_id)
    ).first()

    if not category:
        return {
            "can_delete": False,
            "message": "Category not found or does not belong to user"
        }

    # Check if there are any tasks associated with this category for the user
    associated_task_count = session.exec(
        select(Task)
        .where(Task.category_id == category_id)
        .where(Task.user_id == user_id)
    ).count()

    if associated_task_count > 0:
        return {
            "can_delete": False,
            "message": f"Cannot delete category because it has {associated_task_count} associated task(s)"
        }

    return {
        "can_delete": True,
        "message": "Category can be safely deleted"
    }


def create_category_with_validation(session: Session, user_id: str, name: str, icon: str) -> Category:
    """
    Create a category after validating the input parameters
    """
    # Validate name length (1-50 characters)
    if len(name) < 1 or len(name) > 50:
        raise ValueError("Category name must be between 1 and 50 characters")

    # Validate icon length (1-10 characters)
    if len(icon) < 1 or len(icon) > 10:
        raise ValueError("Category icon must be between 1 and 10 characters")

    # Check if category with same name already exists for this user
    existing_category = session.exec(
        select(Category)
        .where(Category.name == name)
        .where(Category.user_id == user_id)
    ).first()

    if existing_category:
        raise ValueError(f"Category with name '{name}' already exists")

    # Create new category
    new_category = Category(
        name=name,
        icon=icon,
        user_id=user_id,
        created_at=datetime.utcnow()
    )

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category