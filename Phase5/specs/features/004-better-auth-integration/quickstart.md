# Quickstart Guide: Better Auth Integration

## Overview
This guide provides step-by-step instructions to implement Better Auth with JWT tokens for securing your Next.js frontend and FastAPI backend.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- npm or yarn package manager
- uv (for Python dependency management)

## Step 1: Install Better Auth

### Frontend Installation
```bash
cd frontend
npm install better-auth
# or
yarn add better-auth
```

## Step 2: Configure Better Auth with JWT

### Frontend Configuration
Create `lib/auth.ts` in your frontend directory:

```typescript
import { createAuth } from "better-auth";

export const auth = createAuth({
  // Enable JWT plugin
  plugins: [
    {
      name: "JWT",
      hooks: {
        afterSessionCreate: async ({ session }) => {
          // Generate JWT token with user information
          return {
            jwt: generateJWT(session.user),
          };
        },
      },
    },
  ],
  // Other configuration options
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});
```

## Step 3: Set Up Environment Variables

### Frontend Environment (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-secret-here
BETTER_AUTH_URL=http://localhost:3000
```

### Backend Environment (.env)
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-32-character-secret-here  # Must match frontend
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
```

## Step 4: Generate Shared Secret
Create a strong 32-character secret for JWT signing:
```bash
# Generate a cryptographically secure secret
openssl rand -base64 32
```

## Step 5: Implement Frontend Authentication

### Create Auth Provider Component
Create `components/AuthProvider.tsx`:

```tsx
"use client";
import { AuthProvider as BetterAuthProvider } from "better-auth/react";
import { auth } from "@/lib/auth";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return (
    <BetterAuthProvider authClient={auth}>
      {children}
    </BetterAuthProvider>
  );
}
```

### Wrap Application with Auth Provider
Update `app/layout.tsx`:

```tsx
import { AuthProvider } from "@/components/AuthProvider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

## Step 6: Update API Client to Include JWT

### Modify API Client to Include Authorization Header
Update `lib/api.ts`:

```typescript
async function apiCall(endpoint: string, options: RequestInit = {}) {
  // Get JWT token from auth session
  const token = await getAuthToken();

  const headers = {
    "Content-Type": "application/json",
    ...(token && { "Authorization": `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API call failed: ${response.status}`);
  }

  return response.json();
}

// Function to get JWT token from Better Auth session
async function getAuthToken() {
  // Implementation to retrieve JWT token from Better Auth session
  // This would use Better Auth's client-side API to get the token
}
```

## Step 7: Implement Backend JWT Verification

### Install Required Dependencies
```bash
pip install python-jose[cryptography] python-multipart
```

### Create JWT Verification Module
Create `backend/auth.py`:

```python
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

# JWT Configuration
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    email: str

def verify_jwt_token(token: str) -> Optional[TokenData]:
    """
    Verify JWT token and extract user information
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return TokenData(user_id=user_id, email=email)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Get current authenticated user from JWT token
    """
    token_data = verify_jwt_token(credentials.credentials)
    return token_data

def verify_user_access(request_user_id: str, authenticated_user_id: str):
    """
    Verify that the requested user_id matches the authenticated user
    """
    if request_user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: user_id does not match authenticated user"
        )
```

## Step 8: Update API Routes to Require Authentication

### Apply Authentication to Existing Routes
Update your existing task routes in `backend/routes/tasks.py`:

```python
from fastapi import APIRouter, Depends
from auth import get_current_user, verify_user_access, TokenData
from models import Task

router = APIRouter(prefix="/api/{user_id}")

@router.get("/tasks")
async def get_tasks(
    user_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    verify_user_access(user_id, current_user.user_id)
    # Return only tasks belonging to authenticated user
    return get_user_tasks(current_user.user_id)

@router.post("/tasks")
async def create_task(
    user_id: str,
    task: Task,
    current_user: TokenData = Depends(get_current_user)
):
    verify_user_access(user_id, current_user.user_id)
    # Ensure task is created for authenticated user
    task.user_id = current_user.user_id
    return create_new_task(task)

@router.get("/tasks/{id}")
async def get_task(
    user_id: str,
    id: int,
    current_user: TokenData = Depends(get_current_user)
):
    verify_user_access(user_id, current_user.user_id)
    task = get_task_by_id(id)
    if task.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return task
```

## Step 9: Test the Integration

### Frontend Testing
1. Register a new user via the frontend
2. Log in and verify JWT token is stored
3. Make API calls and verify Authorization header is included

### Backend Testing
1. Start the backend server
2. Verify JWT verification middleware works
3. Test that unauthorized requests return 401
4. Test that user isolation works (user A can't access user B's tasks)

## Common Issues and Solutions

### Issue: JWT Token Not Included in API Requests
**Solution**: Verify the API client is correctly retrieving and including the JWT token in the Authorization header

### Issue: Token Verification Fails
**Solution**: Ensure the BETTER_AUTH_SECRET is identical in both frontend and backend environments

### Issue: User Isolation Not Working
**Solution**: Verify that all database queries filter by the authenticated user_id from the JWT token

## Security Considerations

- Store BETTER_AUTH_SECRET securely in environment variables
- Use HTTPS in production to protect JWT tokens in transit
- Implement proper token refresh mechanisms for long-lived sessions
- Monitor for JWT token leaks in logs or client storage