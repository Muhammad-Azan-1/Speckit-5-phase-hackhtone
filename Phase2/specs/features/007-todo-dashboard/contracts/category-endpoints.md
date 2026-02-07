# API Contract: Category Management Endpoints

## Overview
This document specifies the REST API endpoints for category management in the Todo application. The API follows REST conventions and requires JWT authentication for all endpoints.

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

### 1. List User Categories
- **Method**: GET
- **Endpoint**: `/api/categories`
- **Description**: Retrieve all categories for the authenticated user
- **Authentication**: Required (JWT token must match user in token)

#### Success Response
- **Status**: 200 OK
- **Body**: Array of category objects

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token

### 2. Create New Category
- **Method**: POST
- **Endpoint**: `/api/categories`
- **Description**: Create a new category for the authenticated user
- **Authentication**: Required (JWT token must match user in token)

#### Request Body
```json
{
  "name": "Category name (1-50 characters)",
  "icon": "Emoji icon (1-10 characters)"
}
```

#### Success Response
- **Status**: 201 Created
- **Body**: Created category object

#### Error Responses
- **400**: Bad Request - Invalid request body format
- **401**: Unauthorized - Invalid or missing JWT token
- **422**: Unprocessable Entity - Validation errors (name length, invalid emoji, etc.)

### 3. Get Specific Category
- **Method**: GET
- **Endpoint**: `/api/categories/{id}`
- **Description**: Retrieve details of a specific category
- **Authentication**: Required (JWT token must match user in token)

#### Success Response
- **Status**: 200 OK
- **Body**: Category object

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - Category doesn't belong to user
- **404**: Not Found - Category doesn't exist

### 4. Update Category
- **Method**: PUT
- **Endpoint**: `/api/categories/{id}`
- **Description**: Update an existing category for the authenticated user
- **Authentication**: Required (JWT token must match user in token)

#### Request Body
```json
{
  "name": "Category name (1-50 characters)",
  "icon": "Emoji icon (1-10 characters)"
}
```

#### Success Response
- **Status**: 200 OK
- **Body**: Updated category object

#### Error Responses
- **400**: Bad Request - Invalid request body format
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - Category doesn't belong to user
- **404**: Not Found - Category doesn't exist
- **422**: Unprocessable Entity - Validation errors

### 5. Delete Category
- **Method**: DELETE
- **Endpoint**: `/api/categories/{id}`
- **Description**: Permanently delete a category
- **Authentication**: Required (JWT token must match user in token)

#### Success Response
- **Status**: 204 No Content

#### Error Responses
- **401**: Unauthorized - Invalid or missing JWT token
- **403**: Forbidden - Category doesn't belong to user
- **404**: Not Found - Category doesn't exist
- **409**: Conflict - Category has associated tasks (cannot delete)

## Data Models

### Category Object
```json
{
  "id": 123,
  "name": "Category name",
  "icon": "🎨",
  "user_id": "user_identifier",
  "created_at": "2026-01-07T08:00:00Z"
}
```

### Field Constraints
- **id**: Integer, auto-generated primary key
- **name**: String, 1-50 characters
- **icon**: String, 1-10 characters (emoji)
- **user_id**: String, matches authenticated user from JWT
- **created_at**: ISO 8601 timestamp

## Security Requirements
1. All endpoints require valid JWT token in Authorization header
2. Users can only access their own categories
3. Invalid tokens return 401 Unauthorized
4. User ID mismatches return 403 Forbidden
5. Rate limiting applied to prevent abuse