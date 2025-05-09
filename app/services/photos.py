
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Photo, SavedPhoto, PhotoShare, Rating
from ..schemas import PhotoCreate, SavedPhotoCreate, PhotoShareCreate
from typing import List, Optional
from .base import BaseService

class PhotoService(BaseService[Photo, PhotoCreate, PhotoCreate]):
    def __init__(self):
        super().__init__(Photo)

    def get_user_photos(self, db: Session, user_id: int) -> List[Photo]:
        return db.query(Photo).filter(Photo.owner_id == user_id).all()

    def get_feed(self, db: Session, user_id: int, limit: int = 100) -> List[Photo]:
        following = db.query(UserFollow.followed_id).filter(
            UserFollow.follower_id == user_id
        ).subquery()
        
        return db.query(Photo).filter(
            Photo.owner_id.in_(following),
            Photo.is_public == True
        ).order_by(Photo.created_at.desc()).limit(limit).all()

    def get_best_of_day(self, db: Session, user_id: int) -> Optional[Photo]:
        following = db.query(UserFollow.followed_id).filter(
            UserFollow.follower_id == user_id
        ).subquery()
        
        today = datetime.now().date()
        
        return db.query(Photo).join(Rating).filter(
            Photo.owner_id.in_(following),
            func.date(Photo.created_at) == today
        ).group_by(Photo.id).order_by(func.avg(Rating.value).desc()).first()

    def get_average_rating(self, db: Session, photo_id: int) -> Optional[float]:
        result = db.query(func.avg(Rating.value)).filter(
            Rating.photo_id == photo_id
        ).scalar()
        return float(result) if result else None

    def is_saved(self, db: Session, user_id: int, photo_id: int) -> bool:
        return db.query(SavedPhoto).filter(
            SavedPhoto.user_id == user_id,
            SavedPhoto.photo_id == photo_id
        ).first() is not None

class SavedPhotoService:
    def save_photo(self, db: Session, user_id: int, photo_id: int) -> SavedPhoto:
        existing = db.query(SavedPhoto).filter(
            SavedPhoto.user_id == user_id,
            SavedPhoto.photo_id == photo_id
        ).first()
        
        if existing:
            return existing
            
        db_saved = SavedPhoto(user_id=user_id, photo_id=photo_id)
        db.add(db_saved)
        db.commit()
        db.refresh(db_saved)
        return db_saved

    def unsave_photo(self, db: Session, user_id: int, photo_id: int) -> bool:
        saved = db.query(SavedPhoto).filter(
            SavedPhoto.user_id == user_id,
            SavedPhoto.photo_id == photo_id
        ).first()
        
        if saved:
            db.delete(saved)
            db.commit()
            return True
        return False

    def get_saved_photos(self, db: Session, user_id: int) -> List[SavedPhoto]:
        return db.query(SavedPhoto).filter(SavedPhoto.user_id == user_id).all()

class PhotoShareService:
    def share_photo(self, db: Session, photo_id: int, shared_by_id: int, shared_to_id: int) -> PhotoShare:
        db_share = PhotoShare(
            photo_id=photo_id,
            shared_by_id=shared_by_id,
            shared_to_id=shared_to_id
        )
        db.add(db_share)
        db.commit()
        db.refresh(db_share)
        return db_share

    def get_shared_photos(self, db: Session, user_id: int) -> List[PhotoShare]:
        return db.query(PhotoShare).filter(PhotoShare.shared_to_id == user_id).all()

photo_service = PhotoService()
saved_photo_service = SavedPhotoService()
photo_share_service = PhotoShareService()