# Quickstart: AI Agent for Task Management

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL (or Neon for cloud deployment)
- Better Auth configured
- OpenAI API access for ChatKit

## Setup

### 1. Backend Setup

1. Install dependencies:
```bash
cd backend-app
pip install openai-agents python-dotenv
```

2. Add the MCP server and chat endpoint to your application:
```bash
# The MCP server will be available at backend-app/mcp/
# The chat endpoint will be added to routes/chat.py
```

3. Run database migrations to create Conversation and Message tables:
```bash
# Use your existing migration system to create the new tables
# The migration should create conversations and messages tables
```

4. Update your main application to include the chat routes:
```python
# In main.py, add the chat routes
from routes.chat import router as chat_router
app.include_router(chat_router)
```

### 2. Frontend Setup

1. Install ChatKit in the frontend:
```bash
cd frontend
npm install @openai/chatkit
```

2. Create the chat interface:
```bash
# Create src/app/(dashboard)/chat/page.tsx
# This will integrate with the backend chat endpoint
```

3. Update environment variables:
```bash
# In .env.local, add:
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
NEXT_PUBLIC_API_URL=your-backend-url
```

### 3. Environment Configuration

Add the following to your `.env` file in backend-app:
```
OPENAI_API_KEY=your-openai-api-key
MCP_SERVER_URL=http://localhost:8808  # or your MCP server URL
```

## Running the Application

### Backend
```bash
# Start the MCP server
cd backend-app
python mcp_server.py

# Start the main application
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
# Start the frontend
cd frontend
npm run dev
```

## Testing

1. Navigate to the chat interface at `/chat` in your frontend
2. Authenticate using the existing Better Auth system
3. Try natural language commands like:
   - "Add a task to buy groceries"
   - "Show me my pending tasks"
   - "Mark task 1 as complete"
   - "Delete the meeting task"

## MCP Server Integration

The AI Agent communicates with the existing task management system through the MCP server with 5 tools:
- `add_task` - Create new tasks
- `list_tasks` - Retrieve tasks with optional filtering
- `complete_task` - Toggle task completion status
- `delete_task` - Remove tasks
- `update_task` - Modify task details

## Troubleshooting

### ChatKit Domain Allowlist
If the chat interface doesn't load in production:
1. Go to https://platform.openai.com/settings/organization/security/domain-allowlist
2. Add your domain (e.g., your-app.vercel.app)
3. Get the domain key and add it to your frontend environment variables

### Authentication Issues
Ensure JWT tokens are properly passed from the frontend to the backend chat endpoint.

### MCP Server Connectivity
Verify that the MCP server is running and accessible from the backend application.