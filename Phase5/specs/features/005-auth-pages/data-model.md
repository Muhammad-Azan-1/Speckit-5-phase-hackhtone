# Data Model: Authentication Pages with Better Auth Integration

## User Entity (Managed by Better Auth)

Better Auth provides built-in user management, but we need to understand the user data structure for our application:

| Field | Type | Description | Source |
|-------|------|-------------|---------|
| id | String | Unique user identifier | Better Auth |
| email | String | User's email address | Better Auth |
| name | String | User's full name | Better Auth |
| image | String | Profile picture URL | Better Auth (optional) |
| emailVerified | DateTime | When email was verified | Better Auth |
| createdAt | DateTime | Account creation timestamp | Better Auth |
| updatedAt | DateTime | Last update timestamp | Better Auth |

## Form Data Structures

### Registration Form Data
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| email | String | User's email address | Required, valid email format |
| password | String | User's password | Required, minimum 8 characters |
| name | String | User's full name | Required, appropriate length |

### Login Form Data
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| email | String | User's email address | Required, valid email format |
| password | String | User's password | Required |

## JWT Token Structure

When Better Auth issues JWT tokens, they contain user information that our backend will verify:

| Claim | Type | Description |
|-------|------|-------------|
| sub | String | Subject (user ID) |
| email | String | User's email |
| name | String | User's name |
| iat | Integer | Issued at timestamp |
| exp | Integer | Expiration timestamp |

## UI Component Data Models

### Auth Card Component
| Property | Type | Description |
|----------|------|-------------|
| title | String | Card title (e.g., "Welcome Back", "Create Account") |
| description | String | Subtitle or description text |
| children | ReactNode | Child components (usually form) |

### Form State
| Property | Type | Description |
|----------|------|-------------|
| isLoading | Boolean | Whether the form is in a loading state |
| error | String | Error message to display |
| success | String | Success message to display |

## Validation Schemas

### Registration Schema (using Zod)
| Field | Type | Validation Rules |
|-------|------|------------------|
| email | String | Required, email format, max length 255 |
| password | String | Required, min length 8, max length 100 |
| name | String | Required, min length 2, max length 100 |

### Login Schema (using Zod)
| Field | Type | Validation Rules |
|-------|------|------------------|
| email | String | Required, email format |
| password | String | Required, min length 8 |

## Relationship with Existing Task Model

Our existing Task model will be extended with user ownership:

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Task ID (primary key) |
| title | String | Task title |
| description | String | Task description (optional) |
| completed | Boolean | Completion status |
| user_id | String | Owner's user ID (foreign key to Better Auth user) |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Validation Rules

1. **Form Validation**: All form inputs must pass Zod validation before submission
2. **Password Strength**: Passwords must be at least 8 characters
3. **Email Format**: Email addresses must follow standard email format
4. **Name Length**: Names must be between 2 and 100 characters
5. **Token Expiration**: JWT tokens expire after 7 days (configurable)

## State Transitions

### Form State Transitions
- **Initial**: Form loaded, no user input
- **Validating**: Form submitted, validation in progress
- **Submitting**: Valid form data sent to server
- **Success**: Operation completed successfully
- **Error**: Operation failed with error message

### Authentication State Transitions
- **Unauthenticated**: No JWT token present or invalid token
- **Authenticating**: User submitting login/register form
- **Authenticated**: Valid JWT token with user information available
- **Expired**: JWT token exists but has expired

## Security Constraints

1. **Secure Storage**: JWT tokens must be stored securely (preferably in httpOnly cookies)
2. **Transmission Security**: All authentication requests must use HTTPS
3. **Input Validation**: All form data must be validated client-side and server-side
4. **Rate Limiting**: Authentication endpoints must implement rate limiting
5. **Session Management**: Proper session handling with secure logout