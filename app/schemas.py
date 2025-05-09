from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    is_photographer: bool = False
    profile_picture: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    profile_picture: Optional[str] = None

class UserOut(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class UserWithRating(UserOut):
    average_rating: Optional[float] = None

class UserFollowCreate(BaseModel):
    followed_id: int

class UserFollowOut(BaseModel):
    follower_id: int
    followed_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Photo Schemas
class PhotoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: bool = True

class PhotoCreate(PhotoBase):
    pass

class PhotoOut(PhotoBase):
    id: int
    file_path: str
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PhotoWithRating(PhotoOut):
    average_rating: Optional[float] = None
    is_saved: bool = False

class SavedPhotoCreate(BaseModel):
    photo_id: int

class PhotoShareCreate(BaseModel):
    photo_id: int
    shared_to_id: int

class SavedPhotoOut(BaseModel):
    user_id: int
    photo_id: int
    saved_at: datetime

    class Config:
        from_attributes = True

# Rating Schemas
class RatingBase(BaseModel):
    value: float
    photo_id: Optional[int] = None
    photographer_id: Optional[int] = None

class RatingCreate(RatingBase):
    pass

class RatingOut(RatingBase):
    id: int
    rater_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True