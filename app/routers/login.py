from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.schemas.auth import (LoginRequest, TokenResponse)
from app.services.login import login_user

router = APIRouter(tags=["Login"])


@router.post("/login",response_model=TokenResponse)
def login(payload: LoginRequest,db: Session = Depends(get_db)):
    return login_user(db=db,email=payload.email,password=payload.password)