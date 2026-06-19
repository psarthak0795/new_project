from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.database.models.user import User
from app.database.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return UserService.get_my_profile(current_user)


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return UserService.get_all_users(db=db,current_user=current_user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return UserService.get_user_by_id(
        db=db,
        user_id=user_id,
        current_user=current_user)
    
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserResponse,
    db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return UserService.update_user(db,user_id,user_data,current_user)
    
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return UserService.delete_user(
        db=db,user_id=user_id,current_user=current_user)