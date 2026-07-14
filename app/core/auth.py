from fastapi import HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings
from datetime import datetime, timedelta, timezone


def generate_token(user_id: int):
    """
    Generate a JWT token with the given data.

    Args:
        data (dict): The data to include in the token payload.

    Returns:
        str: The generated JWT token.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
        )
    
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }

    token = jwt.encode(
        payload, 
        settings.secret_key, 
        algorithm=settings.algorithm
        )
    
    return token


def verify_token(token:str):
    """
    Verify the given JWT token and return the decoded payload.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict: The decoded payload from the JWT token.
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
