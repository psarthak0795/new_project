from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import  HTTPBearer 
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models.user import User
from app.core.security import (SECRET_KEY,ALGORITHM)
from app.services.refresh import refresh_access_token


def get_current_user(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401,
        detail="Could not validate credentials")
    access_token = request.cookies.get("access_token")
    payload = None

    if access_token:
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            payload = None

    if payload is None:
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token is None:
            raise credentials_exception

        try:
            refreshed = refresh_access_token(refresh_token)
            response.set_cookie(
                key="access_token",
                value=refreshed["access_token"],
                path="/",
                httponly=True,
                max_age=3600,
                samesite="lax"
            )
            payload = jwt.decode(refreshed["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
        except HTTPException:
            raise credentials_exception
        except JWTError:
            raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise credentials_exception

    return user

