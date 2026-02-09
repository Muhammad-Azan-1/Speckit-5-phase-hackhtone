"""
Rate limiting middleware for authentication endpoints
"""
from fastapi import HTTPException, Request, status
from typing import Dict
import time
from collections import defaultdict

# Dictionary to track failed attempts per IP
failed_attempts: Dict[str, list] = defaultdict(list)
BLOCK_DURATION = 300  # 5 minutes in seconds (300 seconds)
MAX_FAILED_ATTEMPTS = 5

class RateLimitMiddleware:
    """
    Middleware to implement rate limiting based on failed authentication attempts
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        path = request.url.path

        # Apply rate limiting to auth-related endpoints
        if self.is_auth_endpoint(path):
            client_ip = self.get_client_ip(scope)

            # Check if IP is rate-limited
            if self.is_rate_limited(client_ip):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many failed authentication attempts. Please try again later."
                )

        return await self.app(scope, receive, send)

    def is_auth_endpoint(self, path: str) -> bool:
        """
        Check if the endpoint is related to authentication
        """
        auth_patterns = [
            '/api/auth/',
            '/login',
            '/register',
            '/signin',
            '/signup',
            '/logout',
            '/verify',
            '/refresh'
        ]

        for pattern in auth_patterns:
            if pattern in path:
                return True
        return False

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
        return len(recent_attempts) >= MAX_FAILED_ATTEMPTS

    def record_failed_attempt(self, ip: str):
        """
        Record a failed authentication attempt for an IP
        """
        failed_attempts[ip].append(time.time())

    def get_client_ip(self, scope) -> str:
        """
        Extract client IP from scope
        """
        headers = dict(scope.get("headers", []))

        # Check for X-Forwarded-For header
        forwarded_for = headers.get(b"x-forwarded-for")
        if forwarded_for:
            return forwarded_for.decode().split(",")[0].strip()

        # Check for X-Real-IP header
        real_ip = headers.get(b"x-real-ip")
        if real_ip:
            return real_ip.decode().strip()

        # Fallback to remote address if available
        for item in scope.get("extensions", {}).get("http", {}).get("values", []):
            if isinstance(item, tuple) and len(item) >= 2 and item[0] == b"client":
                addr, *_ = item[1]
                return addr.decode() if isinstance(addr, bytes) else str(addr)

        return "unknown"

# Utility function to record failed attempts from other parts of the application
def record_failed_auth_attempt(ip: str):
    """
    Record a failed authentication attempt
    """
    failed_attempts[ip].append(time.time())