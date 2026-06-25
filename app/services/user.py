from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models.user import User, UserRole
from app.routers import user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


class UserService:

    def get_my_profile(current_user: User):
        return current_user

    def get_all_users(db: Session, current_user: User):
        if current_user.role != UserRole.manager:
            raise HTTPException(
                status_code=403,
                detail="Only managers can access all users"
            )

        return get_all_users(db)

    def get_user_by_id(
        db: Session,
        user_id: int,
        current_user: User
    ):
        if current_user.role != UserRole.manager:
            raise HTTPException(
                status_code=403,
                detail="Only managers can access user details"
            )

        user = get_user_by_id(db, user_id)
        return user
    
    def update_user(db: Session, user_id: int, user_data: dict, current_user: User):
        if current_user.role != UserRole.manager and current_user.id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Only managers or the profile owner can update user details"
            )

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404,detail="User not found")

        if hasattr(user_data, 'model_dump'):
            update_items = user_data.model_dump(exclude_unset=True)
        else:
            update_items = user_data

        for key, value in update_items.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user
    
    def delete_user(db: Session, user_id: int, current_user: User):
        if current_user.role != UserRole.manager:
            raise HTTPException(
                status_code=403,
                detail="Only managers can delete users"
            )

        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}