# System Architecture: Todo App

## Architecture Overview
The Todo application follows a layered architecture with clear separation of concerns between frontend, backend, and database layers.

## Layered Architecture

### 1. Presentation Layer (Frontend)
- **Technology**: Next.js 16+ with App Router
- **Components**: Server Components (default), Client Components (when needed)
- **Styling**: Tailwind CSS 3+
- **Language**: TypeScript 5+ with strict mode
- **Responsibilities**:
  - User interface rendering
  - User interactions and events
  - Form validation (client-side)
  - State management
  - API communication

### 2. Application Layer (Backend)
- **Technology**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth
- **Responsibilities**:
  - Business logic
  - Authentication and authorization
  - Request/response handling
  - Data validation (server-side)
  - Database operations orchestration

### 3. Data Layer
- **Technology**: Neon PostgreSQL
- **Responsibilities**:
  - Data persistence
  - Integrity constraints
  - Relationships enforcement
  - Indexed queries

## Communication Protocols

### Frontend ↔ Backend
- Protocol: RESTful API over HTTPS
- Data Format: JSON
- Authentication: JWT tokens in `Authorization: Bearer <token>` header
- Error Format: Consistent JSON with detail object

### Backend ↔ Database
- Protocol: SQLModel ORM queries only
- Connection: Connection pooling configured
- Security: Always filter by user_id for user data

## Security Architecture

### Authentication Flow
1. User logs in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend stores token securely
4. Frontend includes token in API requests: `Authorization: Bearer <token>`
5. Backend extracts and verifies JWT signature
6. Backend extracts user_id from token
7. Backend verifies user_id matches requested resource

### Data Isolation
- ALL database queries MUST filter by authenticated user_id
- User ID from JWT token MUST match URL parameter
- NO cross-user data access permitted

## API Design Principles

### RESTful Standards
- URL Structure: `/api/{user_id}/{resource}` for collections
- HTTP Methods: Follow standard conventions (GET, POST, PUT, PATCH, DELETE)
- Status Codes: Follow standard HTTP status codes

### Required API Endpoints
- GET `/api/{user_id}/tasks` - List all user tasks with filtering, sorting, pagination
- POST `/api/{user_id}/tasks` - Create new task
- GET `/api/{user_id}/tasks/{id}` - Get specific task details
- PUT `/api/{user_id}/tasks/{id}` - Update entire task
- DELETE `/api/{user_id}/tasks/{id}` - Delete task permanently
- PATCH `/api/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Database Principles

### Schema Design
- Naming: Lowercase, snake_case, plural names for resources
- Primary Keys: id (integer auto-increment)
- Foreign Keys: {table_name}_id format
- Timestamps: {action}_at format (created_at, updated_at)

### Data Integrity
- Primary keys on all tables
- Foreign key constraints with appropriate ON DELETE rules
- NOT NULL constraints where appropriate
- UNIQUE constraints where needed
- CHECK constraints for business rules
- Indexes for frequently queried columns