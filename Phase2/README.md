# Phase 2: Todo Full-Stack Web Application

## 🎯 Objective
Transform the console app into a modern multi-user web application with persistent storage.

## ✅ Features Implemented
- ✅ All 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
- ✅ RESTful API endpoints
- ✅ Responsive web interface  
- ✅ Neon PostgreSQL database persistence
- ✅ Better Auth with JWT authentication
- ✅ Multi-user support with data isolation

## 🛠️ Technology Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth |

## 🚀 Running the Application

### Backend
```bash
cd backend-app
uv sync
uv run uvicorn main:app --reload
```
API available at: http://localhost:8000

### Frontend  
```bash
cd frontend
npm install
npm run dev
```
Application available at: http://localhost:3000

## 📝 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/{user_id}/tasks | List all user's tasks |
| POST | /api/{user_id}/tasks | Create a new task |
| GET | /api/{user_id}/tasks/{id} | Get task details |
| PUT | /api/{user_id}/tasks/{id} | Update a task |
| DELETE | /api/{user_id}/tasks/{id} | Delete a task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

## 📂 Project Structure
```
Phase2/
├── frontend/           # Next.js application
├── backend-app/        # FastAPI application  
└── specs/              # Feature specifications
```

## 🎓 Development Approach
Built using **Spec-Driven Development** with Claude Code and Spec-Kit Plus.

---
**Submission for**: Hackathon II - Phase 2  
**Points**: 150
