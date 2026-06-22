from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: dict):
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def register_user_service(db: Session, payload):
    existing_user = get_user_by_email(db, payload.email)

    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")

    user_data = payload.model_dump(exclude={"password"})
    user_data["password"] = hash_password(payload.password)

    user = create_user(db, user_data)
    print("user created")
    return {"message": "User created successfully","user_id": user.id}