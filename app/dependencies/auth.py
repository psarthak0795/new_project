from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import  HTTPBearer 
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models.user import User
from app.core.security import (SECRET_KEY,ALGORITHM)


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401,
        detail="Could not validate credentials")
    token = request.cookies.get("access_token")
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (db.query(User).filter(User.id == int(user_id)).first())

    if not user:
        raise credentials_exception

    return user

