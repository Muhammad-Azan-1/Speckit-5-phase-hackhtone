# Data Model: AI Agent for Task Management

## Entity: Conversation
**Description**: Represents a chat session between user and AI assistant

**Fields**:
- `id`: int (Primary Key, Auto-increment)
- `user_id`: str (Foreign Key to users table, indexed)
- `created_at`: datetime (Timestamp when conversation was created)
- `updated_at`: datetime (Timestamp when conversation was last updated)

**Relationships**:
- One-to-many with Message (conversation has many messages)

**Validation Rules**:
- `user_id` is required and must correspond to an existing user
- `created_at` defaults to current timestamp
- `updated_at` updates automatically on changes

## Entity: Message
**Description**: Represents a single message in a conversation

**Fields**:
- `id`: int (Primary Key, Auto-increment)
- `conversation_id`: int (Foreign Key to conversations table, indexed)
- `user_id`: str (Foreign Key to users table, indexed)
- `role`: str (Either "user" or "assistant", indexed)
- `content`: str (The message content, max 10000 characters)
- `created_at`: datetime (Timestamp when message was created)

**Relationships**:
- Many-to-one with Conversation (message belongs to one conversation)

**Validation Rules**:
- `conversation_id` is required and must correspond to an existing conversation
- `user_id` is required and must correspond to an existing user
- `role` must be either "user" or "assistant"
- `content` is required and must be between 1-10000 characters
- `created_at` defaults to current timestamp

## Integration with Existing Models

### Task Model Updates
The existing Task model will be used by the MCP tools to perform operations but will not be modified.

### User Isolation
Both Conversation and Message models enforce user isolation by requiring `user_id` validation in all operations.

## State Transitions
There are no explicit state transitions for these entities, but the Message entity has a `role` field that indicates the direction of communication (user input vs. assistant response).