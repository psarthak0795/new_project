from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (verify_password, create_access_token, create_refresh_token)
from app.database.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def login_user(db: Session,email: str,password: str):
    user = get_user_by_email(db=db,email=email)

    if not user:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    if not verify_password(password,user.password):
        raise HTTPException(status_code=401,detail="Invalid credentials")

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }