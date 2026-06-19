from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.schemas.user import UserCreate
from app.services.authh import register_user_service

router = APIRouter(prefix="/authh",tags=["Authentication"])


@router.post("/register")
def register_user(payload: UserCreate,db: Session = Depends(get_db)):
    return register_user_service(db, payload)