from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
from datetime import datetime
from typing import List
from app.dependencies import get_db, get_current_user, get_current_photographer
from app.schemas import PhotoCreate, PhotoOut, PhotoWithRating, SavedPhotoCreate, PhotoShareCreate, SavedPhotoOut
from app.services.photos import photo_service, saved_photo_service, photo_share_service
from app.core.config import settings
from app.models import User
from typing import Optional

router = APIRouter()

@router.post("/", response_model=PhotoOut, status_code=201)
def upload_photo(
    photo_data: PhotoCreate,
    file: UploadFile = File(...),
    user: User = Depends(get_current_photographer),
    db: Session = Depends(get_db)
):
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.upload_dir, file_name)
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return photo_service.create(db, {**photo_data.dict(), "file_path": file_name, "owner_id": user.id})

@router.get("/{photo_id}", response_model=PhotoWithRating)
def get_photo(
    photo_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    photo = photo_service.get(db, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    avg_rating = photo_service.get_average_rating(db, photo_id)
    is_saved = photo_service.is_saved(db, user.id, photo_id)
    
    return {**photo.__dict__, "average_rating": avg_rating, "is_saved": is_saved}

@router.post("/save", response_model=SavedPhotoOut)
def save_photo(
    saved_photo: SavedPhotoCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return saved_photo_service.save_photo(db, user.id, saved_photo.photo_id)

@router.get("/feed", response_model=List[PhotoOut])
def get_feed(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return photo_service.get_feed(db, user.id)

@router.get("/best-of-day", response_model=Optional[PhotoOut])
def get_best_of_day(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return photo_service.get_best_of_day(db, user.id)