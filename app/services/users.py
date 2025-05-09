from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import User, UserFollow, Rating
from ..schemas import UserUpdate, UserFollowCreate
from typing import List, Optional
from .base import BaseService

class UserService(BaseService[User, None, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        return self.update(db, user_id, user_update)

    def follow_user(self, db: Session, follower_id: int, followed_id: int) -> Optional[UserFollow]:
        if follower_id == followed_id:
            return None
        
        existing = db.query(UserFollow).filter(
            UserFollow.follower_id == follower_id,
            UserFollow.followed_id == followed_id
        ).first()
        
        if existing:
            return existing
            
        db_follow = UserFollow(follower_id=follower_id, followed_id=followed_id)
        db.add(db_follow)
        db.commit()
        db.refresh(db_follow)
        return db_follow

    def unfollow_user(self, db: Session, follower_id: int, followed_id: int) -> bool:
        follow = db.query(UserFollow).filter(
            UserFollow.follower_id == follower_id,
            UserFollow.followed_id == followed_id
        ).first()
        
        if follow:
            db.delete(follow)
            db.commit()
            return True
        return False

    def get_followers(self, db: Session, user_id: int) -> List[UserFollow]:
        return db.query(UserFollow).filter(UserFollow.followed_id == user_id).all()

    def get_following(self, db: Session, user_id: int) -> List[UserFollow]:
        return db.query(UserFollow).filter(UserFollow.follower_id == user_id).all()

    def get_average_rating(self, db: Session, photographer_id: int) -> Optional[float]:
        result = db.query(func.avg(Rating.value)).filter(
            Rating.photographer_id == photographer_id
        ).scalar()
        return float(result) if result else None

user_service = UserService()