# API Contracts: Authentication Pages with Better Auth Integration

## Frontend Authentication Endpoints (UI Components)

### User Registration UI Flow
```
GET /register
```
- **Purpose**: Display registration form to new users
- **Input**: None (renders empty form)
- **Output**: Registration page with email, password, and name fields
- **Auth**: None required
- **Success Response**: `200 OK` with registration form UI
- **Error Responses**: `500 Internal Server Error` (if page fails to load)

### User Login UI Flow
```
GET /login
```
- **Purpose**: Display login form to existing users
- **Input**: None (renders empty form)
- **Output**: Login page with email and password fields
- **Auth**: None required
- **Success Response**: `200 OK` with login form UI
- **Error Responses**: `500 Internal Server Error` (if page fails to load)

## Frontend API Client Functions (in lib/api.ts)

### Registration Function
```
frontend.auth.register(email, password, name)
```
- **Purpose**: Register a new user via Better Auth
- **Input**: {email: string, password: string, name: string}
- **Output**: {success: boolean, user?: User, error?: string}
- **Auth**: None required initially
- **Success Response**: User object and authentication token
- **Error Responses**: `400 Bad Request` (validation), `409 Conflict` (email exists)

### Login Function
```
frontend.auth.login(email, password)
```
- **Purpose**: Authenticate user and obtain JWT token
- **Input**: {email: string, password: string}
- **Output**: {success: boolean, user?: User, token?: string, error?: string}
- **Auth**: None required initially
- **Success Response**: User object and JWT token
- **Error Responses**: `400 Bad Request` (validation), `401 Unauthorized` (invalid credentials)

### Logout Function
```
frontend.auth.logout()
```
- **Purpose**: Clear authentication session
- **Input**: None
- **Output**: {success: boolean, error?: string}
- **Auth**: Required (uses existing token)
- **Success Response**: `200 OK` with confirmation
- **Error Responses**: `401 Unauthorized` (if token invalid)

## Form Validation Requirements

### Registration Form Validation
- **Email**: Required, valid email format, max 255 characters
- **Password**: Required, minimum 8 characters, max 100 characters
- **Name**: Required, minimum 2 characters, max 100 characters
- **Validation Method**: Zod schema validation
- **Display**: Inline validation errors

### Login Form Validation
- **Email**: Required, valid email format
- **Password**: Required, minimum 8 characters
- **Validation Method**: Zod schema validation
- **Display**: Inline validation errors

## UI State Management

### Loading States
- **Form Submission**: Show loading spinner during authentication operations
- **Duration**: Until API response is received
- **Behavior**: Disable form inputs during loading

### Error Handling
- **Validation Errors**: Display inline with respective fields
- **API Errors**: Display toast notification with error message
- **Network Errors**: Display user-friendly message suggesting retry

## Error Response Format

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
| 400 | VALIDATION_ERROR | Form validation failed |
| 401 | UNAUTHORIZED | Invalid credentials or expired token |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Requested resource doesn't exist |
| 409 | CONFLICT | Resource already exists (e.g., email taken) |
| 429 | RATE_LIMITED | Too many requests |
| 500 | SERVER_ERROR | Unexpected server error |

## Security Requirements

### Token Management
- **Storage**: JWT tokens stored securely (preferably httpOnly cookies)
- **Transmission**: All API requests include Authorization header: `Authorization: Bearer <token>`
- **Expiration**: Handle token expiration gracefully with refresh or re-authentication
- **Cleanup**: Clear tokens on logout

### Rate Limiting
- **Threshold**: After 5 failed authentication attempts per IP
- **Duration**: Block for 5 minutes
- **Response**: `429 Too Many Requests` with appropriate message

### Input Sanitization
- **Client Side**: Validate all form inputs using Zod
- **Server Side**: Backend validates all inputs regardless of client validation
- **Special Characters**: Properly handle special characters in inputs