"""
Chat API routes for conversation and message management with AI Agent integration
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List, Optional, Dict, Any
from auth import get_current_user
from db import get_session
from models import Conversation, Message, Task as TaskModel
from datetime import datetime
from pydantic import BaseModel, Field
import httpx
import os
from jose import jwt, JWTError
import openai


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message to the AI agent")
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID (creates new if not provided)")


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: Optional[List[Dict[str, Any]]] = Field(default=None, description="List of tools called during the interaction")


class ConversationUpdate(BaseModel):
    summary: Optional[str] = None


@router.post("/conversations", response_model=Conversation)
async def create_conversation(
    *,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new conversation
    """
    # Create a new conversation record
    conversation = Conversation(
        user_id=current_user_id,
        summary=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


@router.get("/conversations", response_model=List[Conversation])
async def get_user_conversations(
    *,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all conversations for the current user
    """
    # Query conversations filtered by user_id
    statement = select(Conversation).where(Conversation.user_id == current_user_id).order_by(Conversation.created_at.desc())
    results = session.exec(statement).all()
    return results


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    *,
    conversation_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific conversation by ID, ensuring it belongs to the current user
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user_id
    )
    conversation = session.exec(statement).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    return conversation


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    *,
    conversation_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific conversation by ID, ensuring it belongs to the current user
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user_id
    )
    conversation = session.exec(statement).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Delete all messages associated with the conversation first using a direct delete statement
    from sqlmodel import delete
    statement_messages = delete(Message).where(Message.conversation_id == conversation_id)
    session.exec(statement_messages)

    # Now delete the conversation
    session.delete(conversation)
    session.commit()
    return {"message": "Conversation deleted successfully"}


@router.patch("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(
    *,
    conversation_id: int,
    conversation_update: ConversationUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a conversation (e.g., rename)
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user_id
    )
    conversation = session.exec(statement).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )
    
    if conversation_update.summary is not None:
        conversation.summary = conversation_update.summary
        
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation



@router.post("/conversations/{conversation_id}/messages", response_model=Message)
async def create_message(
    *,
    conversation_id: int,
    message_data: dict,  # Using dict for simplicity; would typically use a Pydantic model
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new message in a specific conversation
    """
    # Verify the conversation belongs to the current user
    conv_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user_id
    )
    conversation = session.exec(conv_statement).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Extract message data
    role = message_data.get("role", "user")
    content = message_data.get("content", "")

    # Validate role
    if role not in ["user", "assistant", "system"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'user', 'assistant', or 'system'"
        )

    # Validate content length
    if len(content) > 10000:  # Increased to match data model
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content exceeds 10000 character limit"
        )

    # Create message with summary (first 100 characters of content)
    summary = content[:100] if len(content) > 100 else content

    message = Message(
        conversation_id=conversation_id,
        user_id=current_user_id,
        role=role,
        content=content,
        summary=summary,
        created_at=datetime.utcnow()
    )

    session.add(message)
    session.commit()
    session.refresh(message)

    # Update conversation's updated_at timestamp
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()

    return message


@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_conversation_messages(
    *,
    conversation_id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all messages for a specific conversation, ensuring it belongs to the current user
    """
    # Verify the conversation belongs to the current user
    conv_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user_id
    )
    conversation = session.exec(conv_statement).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )

    # Get messages for the conversation, ordered chronologically
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc())

    messages = session.exec(statement).all()
    return messages


@router.post("/chat", response_model=ChatResponse)
async def process_chat_message_route(
    *,
    request: Request,
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Process a chat message through the AI agent with MCP tools integration
    """
    try:
        # Get or create conversation
        if chat_request.conversation_id:
            # Verify the conversation belongs to the current user
            conversation_stmt = select(Conversation).where(
                Conversation.id == chat_request.conversation_id,
                Conversation.user_id == current_user_id
            )
            conversation = session.exec(conversation_stmt).first()

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied"
                )
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=current_user_id,
                summary=chat_request.message[:100] if len(chat_request.message) > 100 else chat_request.message,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            user_id=current_user_id,
            role="user",
            content=chat_request.message,
            summary=chat_request.message[:100] if len(chat_request.message) > 100 else chat_request.message,
            created_at=datetime.utcnow()
        )
        session.add(user_message)
        session.commit()

        # Auto-set conversation title from first message if not set
        if not conversation.summary:
            # Use first 50 chars of message as title
            conversation.summary = chat_request.message[:50] + ("..." if len(chat_request.message) > 50 else "")
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Get conversation history for context
        history_stmt = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.asc())
        history_messages = session.exec(history_stmt).all()
        
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in history_messages[:-1]  # Exclude the just-added message
        ]

        # Get authorization header for MCP
        auth_header = request.headers.get("authorization", "")

        # Process message with the AI agent
        try:
            from task_agents.runner import process_chat_message

            result = await process_chat_message(
                user_id=current_user_id,
                message=chat_request.message,
                conversation_id=conversation.id,
                conversation_history=conversation_history,
                authorization=auth_header
            )

            ai_response = result.response
            tool_calls = result.tool_calls

        except ImportError as e:
            print(f"Import error: {e}")
            ai_response = f"I received your message but the AI agent is not available. Error: {str(e)}"
            tool_calls = []
        except Exception as e:
            print(f"Agent processing error: {e}")
            import traceback
            traceback.print_exc()
            ai_response = f"I'm having trouble processing your request. Error: {str(e)}"
            tool_calls = []

        # Store assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=current_user_id,
            role="assistant",
            content=ai_response,
            summary=ai_response[:100] if len(ai_response) > 100 else ai_response,
            created_at=datetime.utcnow()
        )
        session.add(assistant_message)
        session.commit()

        # Update conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        return ChatResponse(
            conversation_id=conversation.id,
            response=ai_response,
            tool_calls=tool_calls
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )