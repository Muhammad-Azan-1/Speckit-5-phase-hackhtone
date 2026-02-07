"""
Setup-related endpoints for project initialization
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from sqlmodel import Session
from pydantic import BaseModel
from db import get_session
from models import BackendProject
from auth import get_current_user
import os
import json
from datetime import datetime

router = APIRouter()

class ProjectInitializationRequest(BaseModel):
    project_name: str
    dependencies: Optional[list] = []

class ProjectInitializationResponse(BaseModel):
    project_path: str
    status: str
    created_at: str

@router.post("/api/{user_id}/setup", response_model=ProjectInitializationResponse)
async def initialize_backend_project(
    user_id: str,
    request: ProjectInitializationRequest,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """
    Sets up a new backend project with proper structure and dependencies
    """
    # Validate that the user_id matches the authenticated user
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID does not match authenticated user"
        )

    try:
        # Create project directory structure
        project_path = f"./{request.project_name}"

        # Create the project directory if it doesn't exist
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project directory already exists"
            )

        # Create basic project files
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(f"# {request.project_name}\n\nNew backend project\n")

        with open(os.path.join(project_path, "__init__.py"), "w") as f:
            f.write("")

        # Save project info to database
        project = BackendProject(
            name=request.project_name,
            dependencies=json.dumps(request.dependencies),
            config_files=json.dumps(["pyproject.toml", "README.md"]),
            created_at=datetime.utcnow()
        )

        session.add(project)
        session.commit()
        session.refresh(project)

        return ProjectInitializationResponse(
            project_path=project_path,
            status="initialized",
            created_at=datetime.utcnow().isoformat()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize project: {str(e)}"
        )