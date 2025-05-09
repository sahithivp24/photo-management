from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from .database import get_db
from .core.security import oauth2_scheme, decode_token
from .models import User
from .services.auth import auth_service

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = auth_service.get_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def get_current_photographer(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_photographer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Photographer privileges required"
        )
    return current_user