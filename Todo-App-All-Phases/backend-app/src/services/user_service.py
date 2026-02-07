"""
Service module for user-related operations including default category creation
"""
from sqlmodel import Session, select
from models import Category, User
from datetime import datetime


def create_default_categories_for_new_user(session: Session, user_id: str) -> None:
    """
    Create default categories for a new user
    """
    default_categories = [
        {"name": "Work", "icon": "💼"},
        {"name": "Personal", "icon": "🏠"},
        {"name": "Shopping", "icon": "🛒"},
        {"name": "Health", "icon": "💪"},
        {"name": "Learning", "icon": "🎓"},
    ]

    for category_data in default_categories:
        # Check if category already exists for this user
        existing_category = session.exec(
            select(Category)
            .where(Category.name == category_data["name"])
            .where(Category.user_id == user_id)
        ).first()

        if not existing_category:
            # Create new category
            new_category = Category(
                name=category_data["name"],
                icon=category_data["icon"],
                user_id=user_id,
                created_at=datetime.utcnow()
            )
            session.add(new_category)

    session.commit()


def validate_category_deletion(session: Session, category_id: int, user_id: str) -> bool:
    """
    Validate if a category can be deleted (has no associated tasks)
    """
    from models import Task

    # Check if there are any tasks associated with this category for the user
    task_count = session.exec(
        select(Task)
        .where(Task.category_id == category_id)
        .where(Task.user_id == user_id)
    ).count()

    return task_count == 0