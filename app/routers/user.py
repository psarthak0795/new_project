from datetime import date
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.database.models.user import User, UserRole
from app.database.schemas.user import UserResponse
from app.services.user import UserService
from fastapi.responses import HTMLResponse, RedirectResponse
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


@router.get("/edit/{user_id}", response_class=HTMLResponse)
def edit_profile_page(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id and current_user.role != UserRole.manager:
        return RedirectResponse(url="/users/home", status_code=303)

    user = current_user if user_id == current_user.id else UserService.get_user_by_id(
        db=db, user_id=user_id, current_user=current_user
    )

    if not user:
        return RedirectResponse(url="/users/home", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="editprofilepage.html",
        context={"request": request, "user": user}
    )


@router.post("/edit/{user_id}")
def update_profile(
    user_id: int,
    first_name: str = Form(...),
    middle_name: str | None = Form(None),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    gender: str = Form(...),
    designation: str = Form(...),
    address: str = Form(...),
    zip_code: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    country: str = Form(...),
    dob: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id and current_user.role != UserRole.manager:
        return RedirectResponse(url="/users/home", status_code=303)

    user = current_user if user_id == current_user.id else UserService.get_user_by_id(
        db=db, user_id=user_id, current_user=current_user
    )

    if not user:
        return RedirectResponse(url="/users/home", status_code=303)

    dob_value = date.fromisoformat(dob) if dob else None

    update_data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "gender": gender,
        "designation": designation,
        "address": address,
        "zip_code": zip_code,
        "city": city,
        "state": state,
        "country": country,
        "dob": dob_value,
    }

    UserService.update_user(db=db, user_id=user_id, user_data=update_data, current_user=current_user)
    return RedirectResponse(url="/users/home", status_code=303)


@router.get("/all", response_class=HTMLResponse)
def show_all_users_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).all()
    return templates.TemplateResponse(
        request=request,
        name="alluser.html",
        context={
            "request": request,
            "users": users,
            "is_manager": current_user.role == UserRole.manager,
        },
    )


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