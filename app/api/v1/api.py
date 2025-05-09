from fastapi import APIRouter
from .endpoints import auth, users, photos

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(photos.router, prefix="/photos", tags=["photos"])