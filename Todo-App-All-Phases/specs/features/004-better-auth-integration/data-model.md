# Data Model: Better Auth Integration

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

## JWT Token Structure

When Better Auth issues JWT tokens, they contain user information that our backend will verify:

| Claim | Type | Description |
|-------|------|-------------|
| sub | String | Subject (user ID) |
| email | String | User's email |
| name | String | User's name |
| iat | Integer | Issued at timestamp |
| exp | Integer | Expiration timestamp |

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

1. **User Authentication**: All API requests must include a valid JWT token in the Authorization header
2. **User Isolation**: Users can only access/modify tasks belonging to their user_id
3. **Token Expiration**: JWT tokens expire after 7 days (configurable)
4. **Required Fields**: user_id must match authenticated user from JWT token

## State Transitions

### User Authentication State
- **Unauthenticated**: No JWT token provided or invalid token
- **Authenticated**: Valid JWT token with user information available
- **Expired**: JWT token exists but has expired

### Task Ownership Verification
- **Pending**: API request received, JWT token verification in progress
- **Authorized**: JWT token valid and user_id matches requested resource
- **Forbidden**: JWT token valid but user_id does not match requested resource

## Security Constraints

1. **Access Control**: All database queries must filter by authenticated user_id
2. **Token Verification**: All API requests must pass JWT signature verification
3. **User Matching**: URL parameter {user_id} must match authenticated user from JWT
4. **Data Isolation**: Cross-user data access is strictly prohibited