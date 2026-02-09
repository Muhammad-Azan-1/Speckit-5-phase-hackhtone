# API Contract: Dashboard Statistics Endpoints

## Overview
This document specifies the REST API endpoints for dashboard statistics in the Todo application. The API follows REST conventions and requires JWT authentication for all endpoints.

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

### 1. Get Task Statistics
- **Method**: GET
- **Endpoint**: `/api/tasks/stats`
- **Description**: Retrieve aggregated statistics about user's tasks (total, completed, pending)
- **Authentication**: Required (JWT token must match user in token)

#### Success Response
- **Status**: 200 OK
- **Body**: Statistics object with counts

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token

### 2. Get Category Statistics
- **Method**: GET
- **Endpoint**: `/api/tasks/stats/categories`
- **Description**: Retrieve task count per category for the authenticated user
- **Authentication**: Required (JWT token must match user in token)

#### Success Response
- **Status**: 200 OK
- **Body**: Array of category statistics objects

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token

### 3. Get Today's Tasks
- **Method**: GET
- **Endpoint**: `/api/tasks/today`
- **Description**: Retrieve tasks created or due today for the authenticated user
- **Authentication**: Required (JWT token must match user in token)

#### Query Parameters
| Parameter | Type | Required | Default | Valid Values | Description |
|-----------|------|----------|---------|--------------|-------------|
| limit | integer | No | 5 | 1-50 | Maximum results to return |

#### Success Response
- **Status**: 200 OK
- **Body**: Array of task objects created or due today

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token
- **422**: Unprocessable Entity - Invalid query parameters

## Data Models

### Task Statistics Object
```json
{
  "total": 45,
  "completed": 32,
  "pending": 13
}
```

### Category Statistics Object
```json
{
  "category_id": 1,
  "name": "Work",
  "icon": "💼",
  "count": 12
}
```

### Today's Tasks Response
```json
{
  "tasks": [
    {
      "id": 123,
      "title": "Task title",
      "description": "Optional description",
      "completed": false,
      "category_id": 1,
      "due_time": "14:00",
      "created_at": "2026-01-07T08:00:00Z",
      "updated_at": "2026-01-07T08:00:00Z"
    }
  ],
  "count": 5
}
```

## Security Requirements
1. All endpoints require valid JWT token in Authorization header
2. Users can only access their own statistics
3. Invalid tokens return 401 Unauthorized
4. User ID mismatches return 403 Forbidden
5. Rate limiting applied to prevent abuse