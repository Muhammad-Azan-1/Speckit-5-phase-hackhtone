# Phase 3: Todo AI-Powered Chatbot

## 🎯 Objective
Add AI-powered chatbot interface for managing todos through natural language using MCP server architecture.

## ✅ Features Implemented

### From Phase 2 (All Included)
- ✅ Full-stack web app with authentication
- ✅ Complete CRUD operations
- ✅ Database persistence

### New in Phase 3
- ✅ OpenAI ChatKit conversational interface
- ✅ MCP server with Official MCP SDK
- ✅ OpenAI Agents SDK for natural language processing
- ✅ Database-persisted conversation state (stateless server)
- ✅ AI-powered task management via chat

## 🤖 Natural Language Commands

| User Says | AI Does |
|-----------|---------|
| "Add task to buy groceries" | Creates new task |
| "Show me all my tasks" | Lists all tasks |
| "What's pending?" | Filters pending tasks |
| "Mark task 3 as complete" | Marks task complete |
| "Delete the meeting task" | Finds and deletes task |
| "Change task 1 to 'Call mom'" | Updates task title |

## 🛠️ Technology Stack
| Component | Technology |
|-----------|-----------|
| Frontend UI | OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | Neon PostgreSQL |

## 🏗️ MCP Tools
The MCP server exposes these tools to the AI agent:
- `add_task` - Create new task
- `list_tasks` - Retrieve tasks (with optional filter)
- `complete_task` - Mark task as complete
- `delete_task` - Remove task
- `update_task` - Modify task details

## 🚀 Running the Application

### Backend (includes MCP server)
```bash
cd backend-app
uv sync
uv run uvicorn main:app --reload
```
API available at: http://localhost:8000

### Frontend (with ChatKit)
```bash
cd frontend
npm install
npm run dev
```
Chat interface at: http://localhost:3000/chat

## 📂 Project Structure
```
Phase3/
├── frontend/           # Next.js + ChatKit
├── backend-app/        # FastAPI + Agents SDK + MCP server
└── specs/              # Feature specifications
```

## 🎓 Development Approach
Built using **Spec-Driven Development** with Claude Code and Spec-Kit Plus.

---
**Submission for**: Hackathon II - Phase 3  
**Points**: 200  
**Builds on**: Phase 2
