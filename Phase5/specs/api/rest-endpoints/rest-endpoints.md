# API Specification: REST Endpoints for Todo Application

**Created**: 2026-01-07
**Status**: Draft
**Related Feature**: @specs/features/003-todo-api-endpoints/spec.md

## API Overview

This document specifies the REST API endpoints for the Todo application. The API follows REST conventions and requires JWT authentication for all endpoints.

## Authentication

All endpoints require JWT authentication via the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The JWT token must be obtained through the Better Auth system and must contain the user's identity information.

## Base URL
```
http://localhost:8000/api (development)
https://api.yourdomain.com/api (production)
```

## Common Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| Authorization | Bearer {token} | Yes | JWT token from Better Auth |
| Content-Type | application/json | For POST/PUT/PATCH | Request body format |
| Accept | application/json | Yes | Response format |

## Common Response Format

Successful responses return JSON with the appropriate data structure.
Error responses follow this format:
```json
{
  "detail": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "field": "field_name" (optional)
  }
}
```

## Endpoint Specifications

### 1. List User Tasks
- **Method**: GET
- **Endpoint**: `/api/{user_id}/tasks`
- **Description**: Retrieve all tasks for the specified user with support for filtering, sorting, and pagination
- **Authentication**: Required (JWT token must match user_id)

#### Query Parameters
| Parameter | Type | Required | Default | Valid Values | Description |
|-----------|------|----------|---------|--------------|-------------|
| status | string | No | all | all, pending, completed | Filter by completion status |
| sort | string | No | created | created, updated, title | Field to sort by |
| order | string | No | desc | asc, desc | Sort direction |
| limit | integer | No | 50 | 1-100 | Maximum results per page |
| offset | integer | No | 0 | 0+ | Number of results to skip |

#### Success Response
- **Status**: 200 OK
- **Body**: Array of task objects

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - JWT token user_id doesn't match URL user_id
- **422**: Unprocessable Entity - Invalid query parameters

---

### 2. Create New Task
- **Method**: POST
- **Endpoint**: `/api/{user_id}/tasks`
- **Description**: Create a new task for the specified user
- **Authentication**: Required (JWT token must match user_id)

#### Request Body
```json
{
  "title": "Task title (1-255 characters)",
  "description": "Optional task description (0-1000 characters)"
}
```

#### Success Response
- **Status**: 201 Created
- **Body**: Created task object

#### Error Responses
- **400**: Bad Request - Invalid request body format
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - JWT token user_id doesn't match URL user_id
- **422**: Unprocessable Entity - Validation errors (title length, etc.)

---

### 3. Get Specific Task
- **Method**: GET
- **Endpoint**: `/api/{user_id}/tasks/{id}`
- **Description**: Retrieve details of a specific task
- **Authentication**: Required (JWT token must match user_id)

#### Success Response
- **Status**: 200 OK
- **Body**: Task object

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - JWT token user_id doesn't match URL user_id
- **404**: Not Found - Task doesn't exist

---

### 4. Update Entire Task
- **Method**: PUT
- **Endpoint**: `/api/{user_id}/tasks/{id}`
- **Description**: Replace the entire task with new data
- **Authentication**: Required (JWT token must match user_id)

#### Request Body
```json
{
  "title": "Task title (1-255 characters)",
  "description": "Optional task description (0-1000 characters)",
  "completed": false
}
```

#### Success Response
- **Status**: 200 OK
- **Body**: Updated task object

#### Error Responses
- **400**: Bad Request - Invalid request body format
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - JWT token user_id doesn't match URL user_id
- **404**: Not Found - Task doesn't exist
- **422**: Unprocessable Entity - Validation errors

---

### 5. Delete Task
- **Method**: DELETE
- **Endpoint**: `/api/{user_id}/tasks/{id}`
- **Description**: Permanently delete a task
- **Authentication**: Required (JWT token must match user_id)

#### Success Response
- **Status**: 204 No Content

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - JWT token user_id doesn't match URL user_id
- **404**: Not Found - Task doesn't exist

---

### 6. Toggle Task Completion
- **Method**: PATCH
- **Endpoint**: `/api/{user_id}/tasks/{id}/complete`
- **Description**: Toggle the completion status of a task
- **Authentication**: Required (JWT token must match user_id)

#### Success Response
- **Status**: 200 OK
- **Body**: Updated task object with toggled completion status

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - JWT token user_id doesn't match URL user_id
- **404**: Not Found - Task doesn't exist

## Data Models

### Task Object
```json
{
  "id": 123,
  "title": "Task title",
  "description": "Optional description",
  "completed": false,
  "user_id": "user_identifier",
  "created_at": "2026-01-07T08:00:00Z",
  "updated_at": "2026-01-07T08:00:00Z"
}
```

### Field Constraints
- **id**: Integer, auto-generated primary key
- **title**: String, 1-255 characters
- **description**: String, 0-1000 characters (optional)
- **completed**: Boolean, default false
- **user_id**: String, matches authenticated user from JWT
- **created_at**: ISO 8601 timestamp
- **updated_at**: ISO 8601 timestamp

## Security Requirements

1. All endpoints require valid JWT token in Authorization header
2. User ID in JWT token must match user_id in URL path
3. Users can only access their own data
4. Invalid tokens return 401 Unauthorized
5. User ID mismatches return 403 Forbidden
6. Rate limiting applied to prevent abuse