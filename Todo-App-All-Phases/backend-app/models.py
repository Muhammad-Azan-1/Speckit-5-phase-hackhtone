"""
SQLModel database models based on specification entities
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List
import uuid

class Category(SQLModel, table=True):
    """
    Category entity for organizing tasks
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="Category name", min_length=1, max_length=50)
    icon: str = Field(..., description="Emoji icon for category", max_length=10)
    user_id: str = Field(..., description="User identifier from Better Auth JWT token")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the category was created")


class Task(SQLModel, table=True):
    """
    Task entity with user_id for authentication isolation and category_id for organization
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, description="Task description", max_length=1000)
    completed: bool = Field(default=False, description="Task completion status")
    user_id: str = Field(..., description="User identifier from Better Auth JWT token")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", description="Associated category ID")
    version: int = Field(default=1, description="Version for optimistic locking")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the task was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the task was last updated")


class BackendProject(SQLModel, table=True):
    """
    Backend Project entity based on specification
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="The name of the project")
    description: Optional[str] = Field(default=None, description="Brief description of the project")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the project was initialized")
    dependencies: Optional[str] = Field(default=None, description="List of project dependencies as JSON string")
    config_files: Optional[str] = Field(default=None, description="Configuration files included as JSON string")


class DatabaseConnection(SQLModel, table=True):
    """
    Database Connection entity based on specification
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    connection_string: str = Field(..., description="Database connection string (from environment)")
    driver: str = Field(default="postgresql", description="Database driver (postgresql for Neon)")
    pool_size: int = Field(default=5, description="Connection pool size")
    timeout: int = Field(default=30, description="Connection timeout in seconds")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the connection was created")


class AuthenticationSystem(SQLModel, table=True):
    """
    Authentication System entity based on specification
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    jwt_secret: str = Field(..., description="Secret key for JWT signing (from environment)")
    algorithm: str = Field(default="HS256", description="JWT algorithm (HS256)")
    expiration: int = Field(default=1800, description="Token expiration time in seconds")
    user_id: str = Field(..., description="User identifier from token")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the auth system was created")


class UserPreferences(SQLModel, table=True):
    """
    User Preferences entity
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(..., description="User identifier from Better Auth JWT token", index=True, unique=True)
    theme: str = Field(default="light", description="Theme preference (light/dark)")
    show_completed_tasks: bool = Field(default=True, description="Whether to show completed tasks")
    date_format: str = Field(default="MM/DD/YYYY", description="Date format preference")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when preferences were last updated")


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a chat session between a user and the AI assistant
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(..., description="User identifier from Better Auth JWT token", index=True)
    summary: Optional[str] = Field(default=None, description="Summary of the conversation (first 100 characters)", max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the conversation was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the conversation was last updated")


class Message(SQLModel, table=True):
    """
    Message entity representing an individual message within a conversation
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(..., foreign_key="conversation.id", description="Associated conversation ID", index=True)
    user_id: str = Field(..., description="User identifier from Better Auth JWT token", index=True)
    role: str = Field(..., description="Message role (user/assistant/system)", regex=r"^(user|assistant|system)$")
    content: str = Field(..., description="Message content", max_length=1000)
    summary: Optional[str] = Field(default=None, description="Summary of the message (first 100 characters)", max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the message was created")