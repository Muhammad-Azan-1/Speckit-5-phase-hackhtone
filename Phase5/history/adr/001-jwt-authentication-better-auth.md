# ADR 001: JWT-based Authentication with Better Auth

**Date**: 2026-01-07
**Status**: Accepted
**Authors**: Development Team

## Context

We need to implement authentication for our Todo application to ensure that users can only access their own tasks. The application consists of a Next.js frontend and a FastAPI backend that need to securely communicate user identity.

## Decision

We will use Better Auth with JWT tokens to implement authentication. Better Auth will handle user registration and login on the frontend, issuing JWT tokens that will be included in all API requests to the backend. The backend will verify these tokens to authenticate users and enforce data isolation.

## Alternatives Considered

### Traditional Session-Based Authentication
- **Pros**: Well-understood pattern, server maintains session state
- **Cons**: Requires shared session storage between services, harder to scale, stateful architecture
- **Rejected** because it goes against our goal of maintaining service independence

### OAuth 2.0 with Custom Authorization Server
- **Pros**: Industry standard, supports multiple auth providers
- **Cons**: More complex setup, requires additional infrastructure
- **Rejected** as overkill for this use case

## Consequences

### Positive
- Stateless authentication allowing service independence
- Easy scaling since no shared session state
- Clear user isolation through JWT claims
- Good security with signed tokens

### Negative
- Slightly more complex token management on the frontend
- Need to handle token expiration and refresh

## Implementation Details

- Frontend will use Better Auth to handle user registration/login
- JWT tokens will be included in Authorization header as "Bearer <token>"
- Backend will verify tokens using shared BETTER_AUTH_SECRET
- All API routes will verify that the authenticated user matches the requested user_id