# API Contracts: Better Auth Integration

## Authentication Endpoints (Managed by Better Auth)

### User Registration
```
POST /api/auth/register
```
- **Purpose**: Create a new user account
- **Input**: email, password, name
- **Output**: JWT token, user profile
- **Auth**: None required
- **Success Response**: `200 OK` with token and user data
- **Error Responses**: `400 Bad Request` (validation), `409 Conflict` (email exists)

### User Login
```
POST /api/auth/login
```
- **Purpose**: Authenticate user and issue JWT token
- **Input**: email, password
- **Output**: JWT token, user profile
- **Auth**: None required
- **Success Response**: `200 OK` with token and user data
- **Error Responses**: `400 Bad Request` (validation), `401 Unauthorized` (invalid credentials)

### User Logout
```
POST /api/auth/logout
```
- **Purpose**: Invalidate user session
- **Input**: None
- **Output**: Success confirmation
- **Auth**: Required JWT token
- **Success Response**: `200 OK`
- **Error Responses**: `401 Unauthorized` (invalid token)

### Get Current User
```
GET /api/auth/me
```
- **Purpose**: Get authenticated user profile
- **Input**: None
- **Output**: User profile data
- **Auth**: Required JWT token
- **Success Response**: `200 OK` with user data
- **Error Responses**: `401 Unauthorized` (invalid token)

## Protected API Endpoints (Updated with Authentication)

### List User Tasks
```
GET /api/{user_id}/tasks
```
- **Purpose**: List all tasks for the authenticated user
- **Input**:
  - Path: user_id (must match authenticated user)
  - Query: status, sort, order, limit, offset
- **Output**: Array of task objects
- **Auth**: Required JWT token (user_id must match token)
- **Success Response**: `200 OK` with tasks array
- **Error Responses**:
  - `401 Unauthorized` (no/invalid token)
  - `403 Forbidden` (user_id mismatch)
  - `400 Bad Request` (invalid query parameters)

### Create Task
```
POST /api/{user_id}/tasks
```
- **Purpose**: Create a new task for the authenticated user
- **Input**:
  - Path: user_id (must match authenticated user)
  - Body: {title: string, description?: string}
- **Output**: Created task object
- **Auth**: Required JWT token (user_id must match token)
- **Success Response**: `201 Created` with task data
- **Error Responses**:
  - `401 Unauthorized` (no/invalid token)
  - `403 Forbidden` (user_id mismatch)
  - `400 Bad Request` (validation error)

### Get Specific Task
```
GET /api/{user_id}/tasks/{id}
```
- **Purpose**: Get details of a specific task
- **Input**:
  - Path: user_id (must match authenticated user), id (task ID)
- **Output**: Task object
- **Auth**: Required JWT token (user_id must match token)
- **Success Response**: `200 OK` with task data
- **Error Responses**:
  - `401 Unauthorized` (no/invalid token)
  - `403 Forbidden` (user_id mismatch or task not owned by user)
  - `404 Not Found` (task doesn't exist)

### Update Task
```
PUT /api/{user_id}/tasks/{id}
```
- **Purpose**: Update entire task for the authenticated user
- **Input**:
  - Path: user_id (must match authenticated user), id (task ID)
  - Body: {title: string, description?: string, completed: boolean}
- **Output**: Updated task object
- **Auth**: Required JWT token (user_id must match token)
- **Success Response**: `200 OK` with updated task data
- **Error Responses**:
  - `401 Unauthorized` (no/invalid token)
  - `403 Forbidden` (user_id mismatch or task not owned by user)
  - `400 Bad Request` (validation error)
  - `404 Not Found` (task doesn't exist)

### Delete Task
```
DELETE /api/{user_id}/tasks/{id}
```
- **Purpose**: Delete a task for the authenticated user
- **Input**:
  - Path: user_id (must match authenticated user), id (task ID)
- **Output**: None
- **Auth**: Required JWT token (user_id must match token)
- **Success Response**: `204 No Content`
- **Error Responses**:
  - `401 Unauthorized` (no/invalid token)
  - `403 Forbidden` (user_id mismatch or task not owned by user)
  - `404 Not Found` (task doesn't exist)

### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{id}/complete
```
- **Purpose**: Toggle task completion status for the authenticated user
- **Input**:
  - Path: user_id (must match authenticated user), id (task ID)
  - Body: {completed: boolean}
- **Output**: Updated task object
- **Auth**: Required JWT token (user_id must match token)
- **Success Response**: `200 OK` with updated task data
- **Error Responses**:
  - `401 Unauthorized` (no/invalid token)
  - `403 Forbidden` (user_id mismatch or task not owned by user)
  - `400 Bad Request` (validation error)
  - `404 Not Found` (task doesn't exist)

## Authorization Requirements

### JWT Token Format
All authenticated requests must include:
```
Authorization: Bearer <jwt_token>
```

### Token Verification
- Backend verifies JWT signature using shared BETTER_AUTH_SECRET
- Token expiration is checked (7-day default)
- User information is extracted from token payload
- Requested user_id must match authenticated user from token

### Error Response Format
All error responses follow this structure:
```json
{
  "detail": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "field": "optional field name for validation errors"
  }
}
```

## Common Error Codes

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 401 | UNAUTHORIZED | Missing or invalid JWT token |
| 403 | FORBIDDEN | User_id mismatch or insufficient permissions |
| 400 | VALIDATION_ERROR | Request validation failed |
| 404 | NOT_FOUND | Requested resource doesn't exist |
| 422 | BUSINESS_ERROR | Business logic validation failed |