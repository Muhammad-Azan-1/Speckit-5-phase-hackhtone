"""
Token refresh mechanism for handling JWT token expiration
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import time
from jose import JWTError, jwt
from config import settings
from fastapi import HTTPException, status

class TokenRefreshHandler:
    """
    Handler for refreshing JWT tokens before they expire
    """

    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        Check if a JWT token is expired
        """
        try:
            # Decode token without verification to check expiration
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options={"verify_signature": False})
            exp = payload.get("exp")

            if exp is None:
                return True  # No expiration claim means expired

            # Check if token expires within 5 minutes (threshold for refresh)
            current_time = time.time()
            return exp < (current_time + 300)  # 300 seconds = 5 minutes
        except JWTError:
            return True  # If we can't decode, consider it expired

    @staticmethod
    def refresh_token_if_needed(token: str) -> Optional[str]:
        """
        Refresh the token if it's close to expiration
        """
        if TokenRefreshHandler.is_token_expired(token):
            # In a real implementation, this would call Better Auth's refresh mechanism
            # For now, we'll return None to indicate the token needs to be refreshed
            # by re-authenticating with Better Auth
            return None

        # Token is still valid, return the same token
        return token

    @staticmethod
    def create_refreshed_token(user_data: Dict[str, Any]) -> str:
        """
        Create a new token with updated expiration
        """
        to_encode = user_data.copy()

        # Set new expiration (7 days from now)
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire.timestamp()})

        # Encode the new token
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_user_data_from_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Extract user data from the token without verifying expiration
        """
        try:
            # Decode token without verifying expiration to get user data
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options={"verify_signature": True, "verify_exp": False})
            return payload
        except JWTError:
            return None

def refresh_better_auth_token_if_needed(token: str) -> Optional[str]:
    """
    Wrapper function to refresh Better Auth token if needed
    """
    try:
        # Check if token needs refresh
        if TokenRefreshHandler.is_token_expired(token):
            # Extract user data from expired token
            user_data = TokenRefreshHandler.get_user_data_from_token(token)
            if user_data:
                # Create a new token with extended expiration
                return TokenRefreshHandler.create_refreshed_token(user_data)
            else:
                # Could not extract user data, need to re-authenticate
                return None
        else:
            # Token is still valid
            return token
    except Exception:
        # If any error occurs, return None to indicate re-authentication is needed
        return None