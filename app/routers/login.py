from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from  fastapi.responses import RedirectResponse
from app.database.connection import get_db
from app.database.schemas.auth import (LoginRequest, TokenResponse)
from app.services.login import login_user

router = APIRouter(tags=["Login"])


@router.post("/login",response_model=TokenResponse)
def login(payload: LoginRequest =Depends(LoginRequest.as_form),db: Session = Depends(get_db)):
    
    token = login_user(db=db,email=payload.email,password=payload.password)
    
    response = RedirectResponse(
        url="/users/home",
        status_code=303
    )
    
    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        path="/"
    )
    return response