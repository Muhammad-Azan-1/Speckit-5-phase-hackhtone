# Quickstart Guide: Todo Dashboard

## Development Setup

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- PostgreSQL (or Neon account for serverless)
- npm/yarn (for frontend dependencies)
- uv/pip (for backend dependencies)

### Environment Configuration
Create `.env` files for both frontend and backend:

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-256-bit-secret-here
BETTER_AUTH_URL=http://localhost:3000
```

**Backend (.env):**
```
DATABASE_URL=postgresql://user:pass@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-256-bit-secret-here
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
```

### Installation

1. **Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
# or if using uv:
uv add fastapi sqlmodel "psycopg2-binary>=2.9.0" "PyJWT[crypto]>=2.0.0" better-auth
```

2. **Frontend Setup:**
```bash
cd frontend
npm install
# Install shadcn/ui components:
npx shadcn@latest add card button input textarea dialog tabs checkbox label avatar skeleton toast select
```

## Running the Application

### Development Mode
1. **Start Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. **Start Frontend:**
```bash
cd frontend
npm run dev
```

### Database Setup
1. Run database migrations to create required tables:
```bash
# After backend is running
cd backend
python -c "from db import create_db_and_tables; create_db_and_tables()"
```

2. The system will automatically create default categories for new users.

## Key Endpoints

### Task Management
- `GET /api/{user_id}/tasks` - List user tasks
- `POST /api/{user_id}/tasks` - Create new task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

### Category Management
- `GET /api/categories` - Get user's categories
- `POST /api/categories` - Create new category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Dashboard Statistics
- `GET /api/tasks/stats` - Get task counts
- `GET /api/tasks/stats/categories` - Get category breakdown

### Authentication
- `/api/auth/[...all]/route` - Better Auth endpoints (frontend)
- JWT tokens required for all protected endpoints

## Frontend Structure

### Pages
- `/(dashboard)/dashboard/page.tsx` - Dashboard page
- `/(dashboard)/todos/page.tsx` - Todos page
- `/(dashboard)/settings/page.tsx` - Settings page

### Components
- `@/components/dashboard/` - Dashboard-specific components
- `@/components/todos/` - Todo list components
- `@/components/settings/` - Settings page components
- `@/components/shared/` - Shared UI components (sidebar, header)

### Hooks
- `@/hooks/use-todos.ts` - Todo operations
- `@/hooks/use-categories.ts` - Category operations
- `@/hooks/use-dashboard-stats.ts` - Dashboard statistics

## Development Workflow

1. **Implement Backend First**: Create API endpoints and database models
2. **Test API**: Verify endpoints work with JWT authentication
3. **Build Frontend**: Create UI components and connect to API
4. **Integrate**: Connect frontend to backend with proper error handling
5. **Test**: Verify all user flows work correctly

## Common Commands

- `npm run dev` - Start frontend in development mode
- `uvicorn main:app --reload` - Start backend with hot reload
- `npm run build` - Build frontend for production
- `pytest` - Run backend tests
- `npm run test` - Run frontend tests