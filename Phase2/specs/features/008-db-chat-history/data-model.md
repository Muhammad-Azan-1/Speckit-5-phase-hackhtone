# Data Model: Chat History Database Migration

## Conversation Entity

**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `user_id`: String, NOT NULL, indexed - User identifier from Better Auth JWT token
- `summary`: String, Optional - First 100 characters of conversation for preview
- `created_at`: DateTime, NOT NULL, Default: UTC timestamp
- `updated_at`: DateTime, NOT NULL, Default: UTC timestamp

**Relationships:**
- One-to-many with Message entity (conversation_id foreign key in Message table)

**Validation Rules:**
- user_id must match authenticated user from JWT token
- created_at and updated_at automatically populated by database

## Message Entity

**Fields:**
- `id`: Integer, Primary Key, Auto-increment
- `conversation_id`: Integer, NOT NULL, indexed - Foreign key referencing Conversation.id
- `user_id`: String, NOT NULL, indexed - User identifier from Better Auth JWT token
- `role`: String, NOT NULL - One of 'user', 'assistant', 'system'
- `content`: String, NOT NULL - Message content (max 1000 characters)
- `summary`: String, Optional - First 100 characters of content for preview
- `created_at`: DateTime, NOT NULL, Default: UTC timestamp

**Relationships:**
- Many-to-one with Conversation entity (foreign key relationship)
- Belongs to user (user_id field for isolation)

**Validation Rules:**
- role must be one of 'user', 'assistant', 'system'
- content length must not exceed 1000 characters
- conversation_id must reference existing Conversation
- user_id must match authenticated user from JWT token

## State Transitions

**Conversation:**
- Created when first message is sent in new conversation
- Updated when new messages are added (updates updated_at timestamp)
- Deleted when user deletes conversation (cascading delete for associated messages)

**Message:**
- Created when user or assistant sends a message
- Immutable after creation (no updates to existing messages)

## Indexing Strategy

**Required Indexes:**
1. Conversation table:
   - Primary index: id (auto-created)
   - Foreign key index: user_id (for user isolation queries)
   - Timestamp index: created_at (for chronological queries)

2. Message table:
   - Primary index: id (auto-created)
   - Foreign key index: conversation_id (for conversation lookup)
   - Combined index: (user_id, created_at) (for user-specific chronological queries)
   - Role index: role (for filtering by message type)

## Referential Integrity

- Foreign key constraint: Message.conversation_id → Conversation.id
- Cascade delete: When Conversation is deleted, all associated Messages are deleted
- User isolation: Both tables include user_id for authentication verification