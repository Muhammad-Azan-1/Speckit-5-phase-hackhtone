# Research: Better Auth Integration

## Decision: JWT-based Authentication with Better Auth
**Rationale:** Based on the feature specification, we're implementing Better Auth with JWT tokens to enable secure communication between the Next.js frontend and FastAPI backend.

## Key Findings from Feature Specification

### Better Auth Configuration
- Enable JWT plugin to issue tokens upon user authentication
- Install via: `npm install better-auth`
- Required environment variables:
  - `BETTER_AUTH_SECRET`: Shared secret for JWT signing/verification (minimum 32 characters)
  - `BETTER_AUTH_URL`: Frontend URL (e.g., http://localhost:3000)

### JWT Token Flow
1. User logs in on Frontend → Better Auth creates a session and issues a JWT token
2. Frontend makes API call → Includes the JWT token in the Authorization: Bearer <token> header
3. Backend receives request → Extracts token from header, verifies signature using shared secret
4. Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
5. Backend filters data → Returns only tasks belonging to that user

### Security Benefits
- User Isolation: Each user only sees their own tasks
- Stateless Auth: Backend doesn't need to call frontend to verify users
- Token Expiry: JWTs expire automatically (e.g., after 7 days)
- No Shared DB Session: Frontend and backend can verify auth independently

### Required Changes
| Component | Changes Required |
| :---- | :---- |
| **Better Auth Config** | Enable JWT plugin to issue tokens |
| **Frontend API Client** | Attach JWT token to every API request header |
| **FastAPI Backend** | Add middleware to verify JWT and extract user |
| **API Routes** | Filter all queries by the authenticated user's ID |

### API Behavior Change
- All endpoints require valid JWT token
- Requests without token receive 401 Unauthorized
- Each user only sees/modifies their own tasks
- Task ownership is enforced on every operation

## Alternatives Considered

### Traditional Session-Based Authentication
- **Pros:** Well-understood pattern, server maintains session state
- **Cons:** Requires shared session storage between services, harder to scale, stateful architecture
- **Decision:** Rejected in favor of JWT for its stateless nature and easier service independence

### OAuth 2.0 with Custom Authorization Server
- **Pros:** Industry standard, supports multiple auth providers
- **Cons:** More complex setup, requires additional infrastructure
- **Decision:** Rejected as overkill for this use case; Better Auth provides simpler JWT solution

## Technical Implementation Details

### Frontend Integration
- Better Auth will handle user registration and login
- JWT tokens will be stored securely (likely in httpOnly cookies or secure localStorage)
- API requests will automatically include Authorization header with Bearer token

### Backend Integration
- FastAPI middleware will verify JWT tokens using the same secret as Better Auth
- Extract user information from JWT payload
- Verify that the authenticated user matches the requested user_id in API endpoints
- Filter database queries to only return data owned by the authenticated user

### Shared Secret Management
- Same `BETTER_AUTH_SECRET` must be configured in both frontend and backend
- Should be at least 32 characters (256 bits) for security
- Should be cryptographically random
- Must be stored securely in environment variables

## Dependencies and Tools

### Better Auth
- Package: `better-auth`
- Purpose: Authentication provider that issues JWT tokens
- Installation: `npm install better-auth`

### JWT Libraries
- Frontend: Included in Better Auth
- Backend: Will need JWT verification library for FastAPI (likely `python-jose` or `PyJWT`)

### FastAPI Security
- Will use FastAPI's built-in security features
- JWT Bearer token scheme for authentication
- Custom middleware for token verification and user extraction