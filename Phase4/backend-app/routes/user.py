from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, text
from pydantic import BaseModel
from db import get_session
from models import UserPreferences
from auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/user")

class UserPreferencesUpdate(BaseModel):
    theme: str
    show_completed_tasks: bool
    date_format: str

class UserProfileUpdate(BaseModel):
    name: str

@router.put("/profile")
async def update_profile(
    profile: UserProfileUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update user profile (name) directly in DB"""
    try:
        # Update Better Auth's user table
        # Table name "user" (quoted for Postgres reserved word)
        # Assuming camelCase columns (standard Better Auth) OR snake_case. 
        # We try strict naming first.
        
        # Try standard Better Auth schema (updatedAt)
        session.exec(
            text('UPDATE "user" SET name = :name, "updatedAt" = :updated_at WHERE id = :id'),
            params={
                "name": profile.name, 
                "id": user_id,
                "updated_at": datetime.utcnow()
            }
        )
        session.commit()
    except Exception:
        session.rollback()
        try:
             # Try snake_case (updated_at)
             session.exec(
                text('UPDATE "user" SET name = :name, updated_at = :updated_at WHERE id = :id'),
                params={
                    "name": profile.name, 
                    "id": user_id,
                    "updated_at": datetime.utcnow()
                }
            )
             session.commit()
        except Exception as e2:
             raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e2)}")
    
    return {"success": True, "name": profile.name}

@router.get("/preferences")
async def get_preferences(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get user preferences, creating default if not exists"""
    # user_id is already the string from get_current_user
    statement = select(UserPreferences).where(UserPreferences.user_id == user_id)
    prefs = session.exec(statement).first()
    
    if not prefs:
        # Create default preferences if not exists
        prefs = UserPreferences(user_id=user_id)
        session.add(prefs)
        session.commit()
        session.refresh(prefs)
        
    return prefs

@router.put("/preferences")
async def update_preferences(
    preferences: UserPreferencesUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update user preferences"""
    statement = select(UserPreferences).where(UserPreferences.user_id == user_id)
    prefs = session.exec(statement).first()
    
    if not prefs:
        prefs = UserPreferences(user_id=user_id)
        session.add(prefs)
    
    prefs.theme = preferences.theme
    prefs.show_completed_tasks = preferences.show_completed_tasks
    prefs.date_format = preferences.date_format
    prefs.updated_at = datetime.utcnow()
    
    session.add(prefs)
    session.commit()
    session.refresh(prefs)
    
    return prefs
