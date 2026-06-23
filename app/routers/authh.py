from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.database.connection import get_db
from app.database.schemas.user import UserCreate, UserResponse
from app.services.authh import register_user_service

router = APIRouter(prefix="/authh",tags=["Authentication"])


@router.post("/register")
def register_user(payload: UserCreate = Depends(UserCreate.as_form),db: Session = Depends(get_db)):
    register_user_service(db, payload)
    
    response = RedirectResponse(
        url="/login",
        status_code=303
    )
    
    return response