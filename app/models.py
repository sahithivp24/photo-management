from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_photographer = Column(Boolean, default=False)
    profile_picture = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    photos = relationship("Photo", back_populates="owner")
    followers = relationship("UserFollow", foreign_keys="UserFollow.followed_id", back_populates="followed")
    following = relationship("UserFollow", foreign_keys="UserFollow.follower_id", back_populates="follower")
    ratings_given = relationship("Rating", back_populates="rater")
    saved_photos = relationship("SavedPhoto", back_populates="user")

class UserFollow(Base):
    __tablename__ = "user_follows"
    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    followed_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    file_path = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_public = Column(Boolean, default=True)
    
    owner = relationship("User", back_populates="photos")
    ratings = relationship("Rating", back_populates="photo")
    saved_by = relationship("SavedPhoto", back_populates="photo")
    shares = relationship("PhotoShare", back_populates="photo")

class SavedPhoto(Base):
    __tablename__ = "saved_photos"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    photo_id = Column(Integer, ForeignKey("photos.id"), primary_key=True)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="saved_photos")
    photo = relationship("Photo", back_populates="saved_by")

class PhotoShare(Base):
    __tablename__ = "photo_shares"
    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    shared_by_id = Column(Integer, ForeignKey("users.id"))
    shared_to_id = Column(Integer, ForeignKey("users.id"))
    shared_at = Column(DateTime(timezone=True), server_default=func.now())
    
    photo = relationship("Photo", back_populates="shares")
    shared_by = relationship("User", foreign_keys=[shared_by_id])
    shared_to = relationship("User", foreign_keys=[shared_to_id])

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    rater_id = Column(Integer, ForeignKey("users.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"), nullable=True)
    photographer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    value = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    rater = relationship("User", back_populates="ratings_given")
    photo = relationship("Photo", back_populates="ratings")
    photographer = relationship("User", foreign_keys=[photographer_id])