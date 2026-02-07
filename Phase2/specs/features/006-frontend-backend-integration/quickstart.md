# Quickstart Guide: Frontend-Backend Integration

## Setup Instructions

### 1. Environment Setup

```bash
# Clone repository
git clone <repo-url>
cd todo-phase2

# Install dependencies
cd frontend && npm install && cd ..
cd backend-app && pip install -r requirements.txt && cd ..
```

### 2. Environment Variables

#### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-char-secret-here
BETTER_AUTH_URL=http://localhost:3000
```

#### Backend (`.env`)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-32-char-secret-here
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
```

### 3. Generate Secrets

```bash
# Generate BETTER_AUTH_SECRET (at least 32 characters)
openssl rand -base64 32
```

### 4. Additional Setup Requirements

- **Transaction Handling**: All database operations must be wrapped in transactions
- **Audit Logging**: All task operations must be logged with user_id, timestamp, and action
- **Rate Limiting**: API endpoints limited to 100 requests per minute per user

### 4. Run Services

```bash
# Terminal 1: Start backend
cd backend-app && uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend && npm run dev
```

### 5. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

## Backend Structure

```
backend-app/
├── main.py              # Application entry point
├── models.py            # SQLModel database models
├── routes/              # API route handlers
│   ├── tasks.py         # Task-related endpoints
│   └── auth.py          # Authentication utilities
├── db.py                # Database connection/session management
├── auth.py              # JWT verification utilities
├── config.py            # Configuration settings
└── requirements.txt     # Python dependencies
```

## Frontend Structure

```
frontend/
├── src/
│   ├── app/             # Next.js App Router pages
│   │   ├── (auth)/      # Authentication pages
│   │   ├── (dashboard)/ # Protected pages
│   │   │   └── todos/   # Task management pages
│   │   └── api/         # API route handlers
│   ├── components/      # Reusable UI components
│   │   ├── ui/          # Base UI components
│   │   ├── forms/       # Form components
│   │   └── todos/       # Task-specific components
│   ├── lib/             # Utilities and API client
│   │   └── api.ts       # API client with JWT handling
│   └── hooks/           # Custom React hooks
│       └── use-auth.ts  # Authentication hook
```

## Key Implementation Points

### 1. JWT Token Handling
- Store JWT token securely in frontend
- Include in Authorization header: `Authorization: Bearer <token>`
- Verify signature using shared BETTER_AUTH_SECRET
- Extract user_id from token and validate against URL parameter

### 2. Data Isolation
- All database queries must filter by authenticated user_id
- Validate that URL user_id matches JWT token user_id
- Return 403 Forbidden for unauthorized access attempts

### 3. Optimistic Locking
- Include version field in Task model
- Check version before updates to detect concurrent modifications
- Return 409 Conflict when version mismatch detected

### 4. Rate Limiting
- Implement rate limiting at 100 requests/minute per user
- Return 429 Too Many Requests when limit exceeded
- Apply to all authenticated API endpoints