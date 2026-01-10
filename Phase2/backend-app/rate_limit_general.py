"""
Rate limiting middleware for API endpoints to prevent abuse
"""
from fastapi import Request, HTTPException, status
from typing import Dict
import time
from collections import defaultdict
import hashlib

# Dictionary to track requests per user/IP
user_requests: Dict[str, list] = defaultdict(list)
BLOCK_DURATION = 60  # 1 minute window
MAX_REQUESTS_PER_MINUTE = 100

class APIRateLimitMiddleware:
    """
    Middleware to implement rate limiting for API endpoints based on user_id
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        
        # Skip rate limiting for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
             return await self.app(scope, receive, send)

        path = request.url.path

        # Only apply rate limiting to API endpoints
        if path.startswith("/api/") and not self.is_public_endpoint(path):
            # Extract user_id from the path or from the JWT token if available
            user_identifier = self.extract_user_identifier(scope, request)

            if user_identifier and self.is_rate_limited(user_identifier):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {MAX_REQUESTS_PER_MINUTE} requests per minute."
                )

        return await self.app(scope, receive, send)

    def is_public_endpoint(self, path: str) -> bool:
        """
        Check if the endpoint is public and doesn't require rate limiting
        """
        public_endpoints = [
            "/docs",           # Swagger docs
            "/redoc",          # Redoc docs
            "/openapi.json",   # OpenAPI spec
            "/health",         # Health check
        ]

        for endpoint in public_endpoints:
            if path.startswith(endpoint):
                return True
        return False

    def extract_user_identifier(self, scope, request: Request) -> str:
        """
        Extract user identifier from the request path or JWT token
        For our API, user_id is in the path like /api/{user_id}/tasks
        """
        path = request.url.path

        # Extract user_id from path pattern /api/{user_id}/...
        path_parts = path.strip('/').split('/')
        if len(path_parts) >= 3 and path_parts[0] == 'api':
            user_id = path_parts[1]
            # Verify it's a valid user_id format (not 'tasks', 'docs', etc.)
            if user_id and user_id not in ['tasks', 'auth', 'docs', 'redoc', 'openapi.json', 'health']:
                return f"user_{user_id}"

        # Fallback to IP-based rate limiting if no user_id found in path
        client_ip = self.get_client_ip(scope)
        return f"ip_{client_ip}"

    def is_rate_limited(self, user_identifier: str) -> bool:
        """
        Check if a user is rate-limited based on their request count
        """
        if user_identifier not in user_requests:
            # First request from this user, initialize
            user_requests[user_identifier] = [time.time()]
            return False

        # Get requests in the last minute
        current_time = time.time()
        recent_requests = [req_time for req_time in user_requests[user_identifier]
                          if current_time - req_time < BLOCK_DURATION]

        # Update the list to only include recent requests
        user_requests[user_identifier] = recent_requests

        # Add current request
        user_requests[user_identifier].append(current_time)

        # Check if limit exceeded
        return len(recent_requests) >= MAX_REQUESTS_PER_MINUTE

    def get_client_ip(self, scope) -> str:
        """
        Extract client IP from scope
        """
        headers = dict(scope.get("headers", []))

        forwarded_for = headers.get(b"x-forwarded-for")
        if forwarded_for:
            return forwarded_for.decode().split(",")[0].strip()

        real_ip = headers.get(b"x-real-ip")
        if real_ip:
            return real_ip.decode().strip()

        # Fallback to a default if IP cannot be determined
        return "unknown"