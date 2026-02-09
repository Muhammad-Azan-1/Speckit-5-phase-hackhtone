"""
Middleware for JWT token verification and user extraction
"""
from fastapi import Request, HTTPException, status
from auth import verify_better_auth_token
import time
from typing import Dict, Optional
from collections import defaultdict
import asyncio

# Dictionary to track failed attempts per IP
failed_attempts: Dict[str, list] = defaultdict(list)
BLOCK_DURATION = 300  # 5 minutes in seconds

class JWTMiddleware:
    """
    Middleware to verify JWT tokens and extract user information
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)

        # Extract path and method
        path = request.url.path
        method = request.method

        # Skip authentication for certain public endpoints
        if self.is_public_endpoint(path):
            return await self.app(scope, receive, send)

        # Get client IP
        client_ip = self.get_client_ip(scope)

        # Check if IP is rate-limited
        if self.is_rate_limited(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed authentication attempts. Please try again later."
            )

        # Extract and verify JWT token from Authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid format"
            )

        token = auth_header.split(" ")[1]

        try:
            # Verify the token and extract user info
            user_data = verify_better_auth_token(token)

            # Add user info to request state for downstream handlers
            request.state.current_user = user_data["user_id"]
            request.state.user_email = user_data["email"]
            request.state.token_payload = user_data["payload"]

            # Reset failed attempts for this IP on successful auth
            if client_ip in failed_attempts:
                del failed_attempts[client_ip]

        except HTTPException:
            # Record failed attempt
            self.record_failed_attempt(client_ip)
            raise
        except Exception:
            # Record failed attempt for any other error during verification
            self.record_failed_attempt(client_ip)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        return await self.app(scope, receive, send)

    def is_public_endpoint(self, path: str) -> bool:
        """
        Check if the endpoint is public and doesn't require authentication
        """
        public_endpoints = [
            "/",               # Root path
            "/docs",           # Swagger docs
            "/redoc",          # Redoc docs
            "/openapi.json",   # OpenAPI spec
            "/health",         # Health check
            "/favicon.ico",    # Favicon
            "/api/auth/",      # Auth endpoints handled separately
        ]

        # Check if path starts with any of the public endpoints
        for endpoint in public_endpoints:
            if path.startswith(endpoint):
                return True
        return False

    def get_client_ip(self, scope) -> str:
        """
        Extract client IP from scope
        """
        for item in scope.get("extensions", {}).get("asgi", {}).get("items", []):
            if item.get("type") == "http.client_addr":
                return item.get("addr", "unknown")

        # Fallback to headers if extension not available
        headers = dict(scope.get("headers", []))
        forwarded_for = headers.get(b"x-forwarded-for", b"")
        if forwarded_for:
            return forwarded_for.decode().split(",")[0].strip()

        remote_addr = headers.get(b"x-real-ip", b"")
        if remote_addr:
            return remote_addr.decode().strip()

        return "unknown"

    def is_rate_limited(self, ip: str) -> bool:
        """
        Check if an IP is rate-limited based on failed attempts
        """
        if ip not in failed_attempts:
            return False

        # Get attempts in the last 5 minutes
        current_time = time.time()
        recent_attempts = [attempt_time for attempt_time in failed_attempts[ip]
                          if current_time - attempt_time < BLOCK_DURATION]

        # Update the list to only include recent attempts
        failed_attempts[ip] = recent_attempts

        # If more than 5 failed attempts in the last 5 minutes, rate limit
        return len(recent_attempts) >= 5

    def record_failed_attempt(self, ip: str):
        """
        Record a failed authentication attempt for an IP
        """
        failed_attempts[ip].append(time.time())

# Additional middleware for rate limiting
class RateLimitMiddleware:
    """
    Middleware to implement rate limiting for authentication endpoints
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        path = request.url.path
        method = request.method

        # Only apply rate limiting to auth-related endpoints
        if '/api/auth/' in path or path in ['/login', '/register', '/signin']:
            client_ip = self.get_client_ip(scope)

            if self.is_rate_limited(client_ip):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later."
                )

        return await self.app(scope, receive, send)

    def get_client_ip(self, scope) -> str:
        """
        Extract client IP from scope
        """
        headers = dict(scope.get("headers", []))
        forwarded_for = headers.get(b"x-forwarded-for", b"")
        if forwarded_for:
            return forwarded_for.decode().split(",")[0].strip()

        remote_addr = headers.get(b"x-real-ip", b"")
        if remote_addr:
            return remote_addr.decode().strip()

        return "unknown"

    def is_rate_limited(self, ip: str) -> bool:
        """
        Check if an IP is rate-limited
        """
        # For simplicity, using the same mechanism as JWT middleware
        # In a real implementation, this would have its own tracking
        global failed_attempts
        if ip not in failed_attempts:
            return False

        current_time = time.time()
        recent_attempts = [attempt_time for attempt_time in failed_attempts[ip]
                          if current_time - attempt_time < BLOCK_DURATION]

        return len(recent_attempts) >= 5