from typing import Optional
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate
from ..core.security import get_password_hash, verify_password
from .base import BaseService

class AuthService(BaseService[User, UserCreate, None]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def create_user(self, db: Session, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            password=hashed_password,
            is_photographer=user.is_photographer,
            profile_picture=user.profile_picture
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def count_accounts(self, db: Session, email: str) -> int:
        return db.query(User).filter(User.email == email).count()

auth_service = AuthService()