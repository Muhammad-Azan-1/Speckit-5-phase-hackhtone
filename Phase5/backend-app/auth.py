"""
JWT authentication and user extraction for Better Auth
Uses JWKS for token verification (EdDSA algorithm with PyJWT)
"""
import httpx
from typing import Optional, Dict, Any
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize security scheme for API docs
security = HTTPBearer()

# Cache for JWKS client
_jwks_client: Optional[PyJWKClient] = None

def get_jwks_client() -> PyJWKClient:
    """
    Get or create JWKS client for Better Auth.
    Caches the client for efficiency.
    """
    global _jwks_client
    
    if _jwks_client is None:
        better_auth_url = settings.better_auth_url
        jwks_url = f"{better_auth_url}/api/auth/jwks"
        _jwks_client = PyJWKClient(jwks_url)
    
    return _jwks_client

def verify_better_auth_token(token: str) -> Dict[str, Any]:
    """
    Verify the Better Auth JWT token using JWKS
    """
    try:
        jwks_client = get_jwks_client()
        
        # Get the signing key from JWKS
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # Decode and verify the token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["EdDSA"],
            options={"verify_aud": False}  # Better Auth may not set audience we expect
        )
        
        # Extract user info from payload
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: no user ID in token"
            )
        
        return {
            "user_id": user_id,
            "email": email,
            "payload": payload
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        logger.error(f"JWT verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Get the current user from the Better Auth JWT token
    """
    token = credentials.credentials
    token_data = verify_better_auth_token(token)
    return token_data["user_id"]

def get_current_user_data(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Get the current user's full data from the Better Auth JWT token
    """
    token = credentials.credentials
    token_data = verify_better_auth_token(token)
    return token_data

def verify_user_access(request_user_id: str, authenticated_user_id: str):
    """
    Verify that the requested user_id matches the authenticated user
    """
    if request_user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: user_id does not match authenticated user"
        )


def log_user_access_attempt(request_user_id: str, authenticated_user_id: str, endpoint: str, success: bool = True):
    """
    Log user access attempts for audit purposes
    """
    if success:
        logger.info(f"User {authenticated_user_id} accessed endpoint {endpoint} for user {request_user_id}")
    else:
        logger.warning(f"User {authenticated_user_id} attempted unauthorized access to user {request_user_id} on endpoint {endpoint}")