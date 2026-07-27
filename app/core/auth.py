from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from uuid import UUID


def create_access_token(user_id: UUID) -> str:
    """
    Generate short-lived access token.
    """
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
        )
    
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expires_at
    }
    
    return jwt.encode(
        payload, 
        settings.secret_key, 
        algorithm=settings.algorithm
        )


def create_refresh_token(user_id: UUID) -> tuple[str, datetime]:
    """
    Generate a long-lived refresh token.
    """

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
        )
    
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expires_at
    }

    token = jwt.encode(
        payload, 
        settings.secret_key, 
        algorithm=settings.algorithm
        )

    return token, expires_at


def verify_token(token:str):
    """
    Verify the given JWT token and return the decoded payload.
    """
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
            )
        
        return payload
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
