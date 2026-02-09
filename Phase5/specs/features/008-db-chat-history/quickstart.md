# Quickstart Guide: Chat History Database Foundation

## Overview
This guide explains how to implement the database foundation for the Phase 3 AI Chatbot, including Conversation and Message models with proper user isolation and indexing.

## Prerequisites
- Working knowledge of SQLModel and Python
- Understanding of the existing backend structure
- Familiarity with the current authentication system (Better Auth JWT)

## Steps to Implement

### 1. Add Models to Existing Models File
Add the new Conversation and Message models to `backend-app/models.py`:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

class Conversation(SQLModel, table=True):
    """
    Conversation entity for storing chat sessions with user_id for authentication isolation
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(..., description="User identifier from Better Auth JWT token", index=True)
    summary: Optional[str] = Field(default=None, description="First 100 characters for conversation preview", max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the conversation was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the conversation was last updated")

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Message entity for storing individual chat messages with user_id for authentication isolation
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(..., foreign_key="conversation.id", index=True, description="Associated conversation ID")
    user_id: str = Field(..., description="User identifier from Better Auth JWT token", index=True)
    role: str = Field(..., description="Message role: 'user', 'assistant', or 'system'", regex=r"^(user|assistant|system)$")
    content: str = Field(..., description="Message content", max_length=1000)
    summary: Optional[str] = Field(default=None, description="First 100 characters of content for preview", max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the message was created")

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

### 2. Create Database Migration
Using the existing migration system in the backend-app directory, create a migration for the new tables:

```bash
# Navigate to backend-app directory
cd backend-app

# Create migration (the exact command depends on your migration system)
# If using Alembic:
alembic revision --autogenerate -m "Add Conversation and Message tables for chat history"

# Apply migration
alembic upgrade head
```

### 3. Update Database Initialization
Ensure the new models are registered when creating database tables by updating `backend-app/db.py`:

```python
def create_db_and_tables():
    """Create database tables if they don't exist"""
    from sqlmodel import SQLModel
    # Import the new models to register them with SQLModel
    from models import Conversation, Message
    SQLModel.metadata.create_all(engine)
```

### 4. Verify Implementation
Test that the new tables are created properly and follow the indexing strategy:
- Conversation table has indexes on: id (PK), user_id
- Message table has indexes on: id (PK), conversation_id, user_id
- Foreign key relationship exists between Message.conversation_id and Conversation.id

## API Integration Points
Once the models are implemented, they will be used by:
- Chat endpoint in `backend-app/routes/chat.py` (future implementation)
- MCP server tools for conversation management (future implementation)
- Frontend chat interface for loading conversation history (future implementation)

## Security Considerations
- All queries must filter by user_id to maintain user isolation
- JWT authentication must be validated before any database operations
- Input validation must ensure content doesn't exceed 1000 characters