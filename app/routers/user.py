from fastapi import APIRouter, Depends ,Request
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.database.models.user import User
from app.database.schemas.user import UserResponse
from app.services.user import UserService
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/home", response_class=HTMLResponse)
def get_my_profile(request:Request,
    db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    user = UserService.get_my_profile(
       
        current_user=current_user)
    
    response = templates.TemplateResponse(
        request=request,
        name="homepage.html",
        context={
            "request": request,
            "user" : user,
            "is_manager" : current_user.role.value == "manager"
        }
        
    )
    return response


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