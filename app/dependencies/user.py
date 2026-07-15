from fastapi import Depends, HTTPException
from app.core.auth import verify_token
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.user_service import UserService

security = HTTPBearer()

def get_current_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ):
          
    token = credentials.credentials
    user_id = verify_token(token).get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return user_id


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)