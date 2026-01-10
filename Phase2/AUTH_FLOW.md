# Authentication Flow Documentation

This document explains how authentication works in this application, step-by-step.

---

## Architecture Overview

| Component | Location | Role |
|-----------|----------|------|
| **Frontend** | Vercel (Next.js) | Authentication Server (Issuer) |
| **Backend** | Hugging Face (FastAPI) | Resource Server (Verifier) |
| **Database** | Neon PostgreSQL | User & Session Storage |

---

## Step-by-Step: User Login Flow

### Step 1: User Clicks Login (Browser)

**What happens:**
- User fills in email + password on the Login page.
- Clicks the "Login" button.

**Code involved:**
- `frontend/src/components/forms/login-form.tsx`
- Calls `authClient.signIn.email({ email, password })`

---

### Step 2: Browser → Frontend (Vercel)

**What happens:**
- `auth-client.ts` sends a **POST** request to:
  ```
  https://speckit-5-phase-hackhtone.vercel.app/api/auth/sign-in/email
  ```
- This is the **same Next.js app** (calling itself).

**Code involved:**
- `frontend/src/lib/auth-client.ts` (lines 10-15)
- Uses `process.env.NEXT_PUBLIC_BETTER_AUTH_URL` to determine the base URL.

---

### Step 3: Frontend Handles Auth (Vercel Server)

**What happens:**
1. `route.ts` receives the request.
2. Better Auth library processes the login.
3. Queries the **Neon PostgreSQL** database to verify credentials.
4. If valid, creates a **Session** and **JWT Token**.
5. Sets a **cookie** in the browser response.

**Code involved:**
- `frontend/src/app/api/auth/[...all]/route.ts`
- `frontend/src/lib/auth.ts` (Better Auth configuration)

**Key configuration:**
```typescript
// frontend/src/lib/auth.ts
export const auth = betterAuth({
    database: pool,                    // Neon PostgreSQL connection
    secret: process.env.BETTER_AUTH_SECRET,  // Token signing secret
    // ...
});
```

---

### Step 4: User is Logged In (Browser)

**What happens:**
- The browser receives the JWT token (stored in cookie).
- `authClient.useSession()` hook detects the active session.
- The UI updates to show "Welcome, [User]!" instead of the login form.

**Code involved:**
- `frontend/src/lib/auth-client.ts` (useSession export)
- Used in various components to check login state.

---

### Step 5: User Fetches Data (Browser → Backend)

**What happens:**
- User navigates to Dashboard or Tasks page.
- Frontend sends a **GET** request to the Backend:
  ```
  https://azan1-todo-app-backend.hf.space/api/tasks
  ```
- The request includes the JWT Token in the **Authorization header**:
  ```
  Authorization: Bearer <JWT_TOKEN>
  ```

**Code involved:**
- `frontend/src/lib/api.ts` (API client with interceptors)
- `frontend/src/hooks/use-tasks.ts`

---

### Step 6: Backend Verifies Token (Hugging Face)

**What happens:**
1. FastAPI receives the request with the Bearer token.
2. `auth.py` extracts the token from the Authorization header.
3. Calls the **Frontend's JWKS endpoint** to get public keys:
   ```
   https://speckit-5-phase-hackhtone.vercel.app/api/auth/jwks
   ```
4. Verifies the token signature using EdDSA algorithm.
5. If valid, extracts `user_id` and `email` from the token payload.
6. Proceeds to fetch the user's data from the database.

**Code involved:**
- `backend-app/auth.py` (lines 22-34, 36-85)

**Key configuration:**
```python
# backend-app/auth.py
def get_jwks_client():
    better_auth_url = settings.better_auth_url  # From environment
    jwks_url = f"{better_auth_url}/api/auth/jwks"
    return PyJWKClient(jwks_url)
```

---

### Step 7: Backend Returns Data

**What happens:**
- If token is valid, the backend queries the database for the user's tasks/categories.
- Returns the data as JSON.
- Frontend receives and displays it.

---

## Visual Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER BROWSER                               │
└─────────────────────────────────────────────────────────────────────────┘
           │                                           │
           │ (1) Login Request                         │ (5) Fetch Tasks
           │ POST /api/auth/sign-in/email              │ GET /api/tasks
           ▼                                           ▼
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│       VERCEL (Next.js)          │     │   HUGGING FACE (FastAPI)        │
│       Authentication Server     │     │   Resource Server               │
│                                 │     │                                 │
│  /api/auth/sign-in/email        │     │  /api/tasks                     │
│  /api/auth/sign-up/email        │     │  /api/categories                │
│  /api/auth/get-session          │     │  /api/dashboard                 │
│  /api/auth/jwks  ◄──────────────┼─────┼── (6) Verify Token              │
│                                 │     │                                 │
└─────────────────────────────────┘     └─────────────────────────────────┘
           │                                           │
           │ (3) Query/Store User                      │ (7) Query Tasks
           ▼                                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         NEON POSTGRESQL DATABASE                         │
│                                                                         │
│   Tables: user, session, account, verification, task, category          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Environment Variables Required

### Frontend (Vercel)
| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend URL (Hugging Face) for fetching tasks |
| `BETTER_AUTH_SECRET` | Secret key for signing JWT tokens |
| `BETTER_AUTH_URL` | This app's public URL |
| `DATABASE_URL` | Neon PostgreSQL connection string |

### Backend (Hugging Face)
| Variable | Purpose |
|----------|---------|
| `BETTER_AUTH_URL` | Frontend URL (Vercel) for JWKS verification |
| `BETTER_AUTH_SECRET` | Same secret as Frontend (for validation) |
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `CORS_ORIGINS` | Allowed frontend origins |

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `frontend/src/lib/auth.ts` | Better Auth server configuration |
| `frontend/src/lib/auth-client.ts` | Browser-side auth client |
| `frontend/src/app/api/auth/[...all]/route.ts` | Auth API endpoints |
| `backend-app/auth.py` | JWT verification for FastAPI |
| `backend-app/config.py` | Environment settings |
