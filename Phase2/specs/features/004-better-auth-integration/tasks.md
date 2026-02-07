# Tasks: Better Auth Integration with Frontend and Backend

## Feature Overview
**Feature**: Better Auth Integration with Frontend and Backend
**Branch**: `004-better-auth-integration`
**Spec**: [specs/features/004-better-auth-integration/spec.md](file:///Users/muhammadazan/Developer/todo-phase2/specs/features/004-better-auth-integration/spec.md)
**Plan**: [specs/features/004-better-auth-integration/plan.md](file:///Users/muhammadazan/Developer/todo-phase2/specs/features/004-better-auth-integration/plan.md)

Integrating Better Auth with JWT tokens to secure the Next.js frontend and FastAPI backend, enabling user authentication and data isolation.

## Implementation Strategy
- MVP: User authentication with JWT token flow
- Incremental: Build authentication first, then secure API endpoints
- Test-driven: Validate authentication and user isolation

## Dependencies
- Next.js frontend must be set up (001-nextjs-frontend)
- FastAPI backend must be set up (002-uv-fastapi-backend)
- Todo API endpoints must be available (003-todo-api-endpoints)

## Parallel Execution Examples
- Frontend auth configuration can be developed in parallel with backend JWT verification
- User registration UI can be developed in parallel with login functionality

---

## Phase 1: Setup and Environment Configuration

- [X] T001 Create BETTER_AUTH_SECRET environment variable in both frontend and backend with 32+ character cryptographically random value using: `openssl rand -base64 32`
- [X] T002 Set up BETTER_AUTH_URL environment variable to http://localhost:3000 in both services
- [X] T003 Install better-auth package in frontend: npm install better-auth
- [X] T004 Create shared configuration documentation for authentication secrets

## Phase 2: Foundational Components

- [X] T005 [P] Create JWT verification module in backend (auth.py) using python-jose
- [X] T006 [P] Create Better Auth configuration in frontend (lib/auth.ts)
- [X] T007 [P] Update frontend API client to include Authorization header with JWT tokens
- [X] T008 [P] Create middleware in backend to extract user info from JWT tokens
- [X] T008a [P] Implement rate limiting middleware for authentication endpoints (5 failed attempts)
- [X] T008b [P] Implement JWT token refresh mechanism for 7-day expiration handling

---

## Phase 3: [US1] Configure Better Auth in Frontend (Priority: P1)

As a user, I want to be able to register and log in to the application so that I can access my personal todo list securely.

**Independent Test**: A user can register for an account, log in, and maintain a session that persists across page refreshes.

- [X] T009 [US1] Create Better Auth client configuration in frontend (lib/auth.ts)
- [X] T010 [US1] Implement user registration form component
- [X] T011 [US1] Implement user login form component
- [X] T012 [US1] Create authentication context/provider to manage user session state
- [X] T013 [US1] Implement session persistence across page refreshes
- [X] T014 [US1] Create protected route component that redirects unauthenticated users
- [X] T015 [US1] Add JWT token retrieval function to include in API requests
- [X] T016 [US1] Test user registration and login functionality with UI

## Phase 4: [US2] Secure Backend API with JWT Verification (Priority: P1)

As a system administrator, I want the backend API to verify JWT tokens from Better Auth so that unauthorized users cannot access or manipulate data.

**Independent Test**: The backend successfully verifies JWT tokens issued by Better Auth and rejects requests with invalid or missing tokens.

- [X] T017 [US2] Implement JWT verification middleware in FastAPI backend
- [X] T018 [US2] Create function to decode and validate JWT tokens from Better Auth
- [X] T019 [US2] Add 401 Unauthorized response for invalid/missing tokens
- [X] T020 [US2] Create dependency for getting current user from JWT token
- [X] T021 [US2] Test JWT verification with valid and invalid tokens
- [X] T022 [US2] Test 401 responses for requests without tokens
- [X] T023 [US2] Test 401 responses for requests with expired tokens
- [X] T023a [US2] Implement JWT token refresh mechanisms when tokens expire (tokens expire after 7 days)
- [X] T023b [US2] Implement rate limiting functionality after 5 failed authentication attempts per IP

## Phase 5: [US3] User Data Isolation (Priority: P1)

As a user, I want to only see and modify my own tasks so that my data remains private and secure from other users.

**Independent Test**: Each user can only access and modify their own data, regardless of what user_id is specified in the URL.

- [X] T024 [US3] Update task model to include user_id field linking to Better Auth user
- [X] T025 [US3] Create function to verify user access to requested resources
- [X] T025a [US3] Implement audit logging for user data access operations
- [X] T026 [US3] Update GET /api/{user_id}/tasks to filter by authenticated user
- [X] T027 [US3] Update POST /api/{user_id}/tasks to assign task to authenticated user
- [X] T028 [US3] Update GET /api/{user_id}/tasks/{id} to verify user owns the task
- [X] T029 [US3] Update PUT /api/{user_id}/tasks/{id} to verify user owns the task
- [X] T030 [US3] Update DELETE /api/{user_id}/tasks/{id} to verify user owns the task
- [X] T031 [US3] Update PATCH /api/{user_id}/tasks/{id}/complete to verify user owns the task
- [X] T032 [US3] Test that user A cannot access user B's tasks
- [X] T033 [US3] Test that user A cannot modify user B's tasks
- [X] T033a [US3] Log all attempts to access other users' data with appropriate details

## Phase 6: [US4] Configure Shared Authentication Secret (Priority: P2)

As a developer, I want to configure the same authentication secret in both frontend and backend so that JWT tokens can be properly issued and verified across services.

**Independent Test**: JWT tokens issued by Better Auth can be successfully verified by the FastAPI backend.

- [X] T034 [US4] Verify BETTER_AUTH_SECRET is identical in frontend and backend environments
- [X] T035 [US4] Create shared configuration validation function
- [X] T036 [US4] Test JWT token issuance from frontend
- [X] T037 [US4] Test JWT token verification by backend with same secret
- [X] T038 [US4] Document the shared secret configuration process

---

## Phase 7: Integration and Testing

- [X] T039 Integrate frontend auth with backend API calls to include JWT tokens
- [X] T040 Test complete user flow: registration → login → API access → logout
- [X] T041 Test user data isolation with multiple user accounts
- [X] T042 Test JWT token expiration and refresh mechanisms
- [X] T043 Verify all API endpoints properly require and verify authentication
- [X] T044 Test error handling for authentication failures
- [X] T045 Update documentation with authentication flow diagrams

## Phase 8: Polish and Cross-Cutting Concerns

- [X] T046 Add loading states and error handling for authentication operations
- [X] T047 Create reusable authentication components for consistent UX
- [X] T048 Add proper error messages for authentication failures
- [X] T049 Update UI to reflect authentication state (login/logout buttons)
- [X] T050 Add rate limiting for authentication endpoints (after 5 failed attempts)
- [X] T051 Document security considerations and best practices
- [X] T052 Clean up temporary files and configurations
- [X] T053 Update README with authentication setup instructions