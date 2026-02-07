# Feature Specification: Better Auth Integration with Frontend and Backend

**Feature Branch**: `004-better-auth-integration`
**Created**: 2026-01-07
**Status**: Draft
**Input**: User description: "now we need to configure the better-auth with frontend and backend here are some detail note that you have also skills called fetch-library-docs you can also use that to understand latest implmentations

Details :
# **Securing the REST API**

*Better Auth \+ FastAPI Integration*

# **The Challenge**

Better Auth is a JavaScript/TypeScript authentication library that runs on your **Next.js frontend**. However, your **FastAPI backend** is a separate Python service that needs to verify which user is making API requests.

# **The Solution: JWT Tokens**

Better Auth can be configured to issue **JWT (JSON Web Token)** tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.

# **How It Works**

* User logs in on Frontend → Better Auth creates a session and issues a JWT token
* Frontend makes API call → Includes the JWT token in the Authorization: Bearer \<token\> header
* Backend receives request → Extracts token from header, verifies signature using shared secret
* Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
* Backend filters data → Returns only tasks belonging to that user

# **What Needs to Change**

| Component | Changes Required |
| :---- | :---- |
| **Better Auth Config** | Enable JWT plugin to issue tokens |
| **Frontend API Client** | Attach JWT token to every API request header |
| **FastAPI Backend** | Add middleware to verify JWT and extract user |
| **API Routes** | Filter all queries by the authenticated user's ID |

# **The Shared Secret**

Both frontend (Better Auth) and backend (FastAPI) must use the **same secret key** for JWT signing and verification. This is typically set via environment variable **BETTER\_AUTH\_SECRET** in both services.

# **Security Benefits**

| Benefit | Description |
| :---- | :---- |
| **User Isolation** | Each user only sees their own tasks |
| **Stateless Auth** | Backend doesn't need to call frontend to verify users |
| **Token Expiry** | JWTs expire automatically (e.g., after 7 days) |
| **No Shared DB Session** | Frontend and backend can verify auth independently |

# **API Behavior Change**

**After Auth:**

| All endpoints require valid JWT token |
| :---- |
| Requests without token receive 401 Unauthorized |
| Each user only sees/modifies their own tasks |
| Task ownership is enforced on every operation |

# **Bottom Line**

The REST API endpoints stay the same (**GET /api/user\_id/tasks**, **POST /api/user\_id/tasks**, etc.), but every request now must include a JWT token, and all responses are filtered to only include that user's data.


adding better-auth you can search using skills but here are also some commands
npm install better-auth
.env BETTER_AUTH_SECRET= , BETTER_AUTH_URL=

ultrathink

create a detials Accurate specification"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Configure Better Auth in Frontend (Priority: P1)

As a user, I want to be able to register and log in to the application so that I can access my personal todo list securely.

**Why this priority**: This is the foundational authentication functionality that enables secure access to the application and establishes user identity for all subsequent operations.

**Independent Test**: A user can register for an account, log in, and maintain a session that persists across page refreshes.

**Acceptance Scenarios**:

1. **Given** I am a new user, **When** I visit the registration page and submit valid credentials, **Then** a new account is created and I am logged in automatically.
2. **Given** I have an existing account, **When** I visit the login page and submit correct credentials, **Then** I am authenticated and redirected to my dashboard.
3. **Given** I am logged in, **When** I refresh the page, **Then** my authentication state is maintained without requiring re-login.
4. **Given** I am logged in, **When** I make API requests to the backend, **Then** the requests automatically include my JWT token in the Authorization header.

---

### User Story 2 - Secure Backend API with JWT Verification (Priority: P1)

As a system administrator, I want the backend API to verify JWT tokens from Better Auth so that unauthorized users cannot access or manipulate data.

**Why this priority**: Security is paramount to protect user data and ensure that users can only access their own information.

**Independent Test**: The backend successfully verifies JWT tokens issued by Better Auth and rejects requests with invalid or missing tokens.

**Acceptance Scenarios**:

1. **Given** a valid JWT token from Better Auth, **When** a request is made to a protected API endpoint, **Then** the request is processed and the appropriate data is returned.
2. **Given** an invalid or expired JWT token, **When** a request is made to a protected API endpoint, **Then** a 401 Unauthorized response is returned.
3. **Given** no JWT token in the request, **When** a request is made to a protected API endpoint, **Then** a 401 Unauthorized response is returned.
4. **Given** a valid JWT token with user information, **When** a request is made to a user-specific endpoint, **Then** the backend verifies that the requesting user matches the requested data scope.

---

### User Story 3 - User Data Isolation (Priority: P1)

As a user, I want to only see and modify my own tasks so that my data remains private and secure from other users.

**Why this priority**: Data privacy and security are critical for user trust and compliance with privacy regulations.

**Independent Test**: Each user can only access and modify their own data, regardless of what user_id is specified in the URL.

**Acceptance Scenarios**:

1. **Given** I am logged in as User A, **When** I request my task list, **Then** only tasks belonging to User A are returned.
2. **Given** I am logged in as User A, **When** I attempt to access User B's task list, **Then** I receive an appropriate error or empty response.
3. **Given** I am logged in as User A, **When** I attempt to create a task for User B, **Then** the task is created under my own user_id regardless of what user_id is specified in the request.
4. **Given** I am logged in as User A, **When** I attempt to modify User B's tasks, **Then** the request is rejected with an appropriate error.

---

### User Story 4 - Configure Shared Authentication Secret (Priority: P2)

As a developer, I want to configure the same authentication secret in both frontend and backend so that JWT tokens can be properly issued and verified across services.

**Why this priority**: Proper authentication requires a shared secret for token signing and verification between services.

**Independent Test**: JWT tokens issued by Better Auth can be successfully verified by the FastAPI backend.

**Acceptance Scenarios**:

1. **Given** the same BETTER_AUTH_SECRET is configured in both frontend and backend, **When** Better Auth issues a JWT token, **Then** the FastAPI backend can successfully verify and decode the token.
2. **Given** different authentication secrets in frontend and backend, **When** Better Auth issues a JWT token, **Then** the FastAPI backend rejects the token as invalid.
3. **Given** the shared secret configuration, **When** the application starts, **Then** both services initialize without authentication errors.

---

### Edge Cases

- What happens when the JWT token expires during a long-running operation?
- How does the system handle clock skew between frontend and backend servers?
- What occurs when the BETTER_AUTH_SECRET is changed - do existing tokens become invalid immediately?
- How does the system handle concurrent requests from the same user with different tokens?
- What happens when a user is deleted but still has valid tokens?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST integrate Better Auth into the Next.js frontend application with email/password and social authentication
- **FR-002**: System MUST configure Better Auth to issue JWT tokens upon successful authentication
- **FR-003**: System MUST install Better Auth using npm install better-auth command
- **FR-004**: System MUST configure BETTER_AUTH_SECRET environment variable for token signing (minimum 32 characters)
- **FR-005**: System MUST configure BETTER_AUTH_URL environment variable for authentication endpoints (set to frontend URL, e.g., http://localhost:3000)
- **FR-006**: System MUST attach JWT tokens to all API requests from frontend to backend
- **FR-007**: System MUST implement JWT verification middleware in FastAPI backend
- **FR-008**: System MUST verify that the authenticated user matches the requested user_id in API endpoints
- **FR-009**: System MUST filter all data queries by the authenticated user's ID
- **FR-010**: System MUST reject requests without valid JWT tokens with 401 Unauthorized status
- **FR-011**: System MUST ensure users can only access their own data regardless of URL parameters
- **FR-012**: System MUST implement proper error handling for authentication failures
- **FR-013**: System MUST implement rate limiting after 5 failed authentication attempts
- **FR-014**: System MUST maintain user session state across page navigations
- **FR-015**: System MUST implement proper token refresh mechanisms when tokens expire (tokens expire after 7 days)
- **FR-016**: System MUST configure Better Auth MCP server as specified in the requirements
- **FR-017**: System MUST use HS256 (HMAC-SHA256) algorithm for JWT token signing and verification

### Key Entities *(include if feature involves data)*

- **User Session**: The authenticated state of a user that persists across requests and page refreshes
- **JWT Token**: A JSON Web Token containing user identity information that is signed with a shared secret
- **Authentication Secret**: The shared secret key used by both frontend (Better Auth) and backend (FastAPI) for JWT signing and verification
- **User Identity**: The verified identity of a user that determines their access rights and data scope

## Clarifications

### Session 2026-01-07

- Q: What is the JWT token expiration time? → A: 7 days
- Q: What is the minimum length for BETTER_AUTH_SECRET? → A: 32 characters
- Q: What should BETTER_AUTH_URL be set to? → A: http://localhost:3000
- Q: What authentication providers should be supported? → A: Email/password and social authentication
- Q: How many failed attempts before rate limiting? → A: 5 failed attempts

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can successfully register and log in with Better Auth in under 30 seconds
- **SC-002**: All API requests from frontend to backend include valid JWT tokens in Authorization header
- **SC-003**: Backend successfully verifies JWT tokens and rejects invalid requests with 401 status
- **SC-004**: Users can only access their own data, with zero cross-user data leakage
- **SC-005**: Authentication state persists across page refreshes and navigations
- **SC-006**: The system handles token expiration gracefully with automatic refresh or re-authentication
- **SC-007**: Better Auth MCP server is properly configured and operational
- **SC-008**: Registration and login success rates exceed 95% under normal operating conditions
- **SC-009**: JWT tokens are signed and verified using HS256 algorithm as required by constitution