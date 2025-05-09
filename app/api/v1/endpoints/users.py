from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas import UserUpdate, UserFollowCreate, UserWithRating, UserOut, UserFollowOut
from app.services.users import user_service
from app.models import User

router = APIRouter()

@router.get("/me", response_model=UserWithRating)
def read_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    avg_rating = None
    if current_user.is_photographer:
        avg_rating = user_service.get_average_rating(db, current_user.id)
    return {**current_user.__dict__, "average_rating": avg_rating}

@router.put("/me", response_model=UserOut)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return user_service.update_user(db, current_user.id, user_update)

@router.post("/follow", response_model=UserFollowOut)
def follow_user(
    follow: UserFollowCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = user_service.follow_user(db, current_user.id, follow.followed_id)
    if not result:
        raise HTTPException(status_code=400, detail="Unable to follow user")
    return result

@router.delete("/unfollow/{followed_id}")
def unfollow_user(
    followed_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not user_service.unfollow_user(db, current_user.id, followed_id):
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    return {"detail": "Successfully unfollowed"}