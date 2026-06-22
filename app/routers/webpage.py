from fastapi import APIRouter, Request 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

#for register page
@router.get("/register",response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )

#for login page
@router.get("/login",response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="loginpage.html",
        context={"request": request}
    )
    
#for home page 
@router.get("/home",response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="homepage.html",
        context={"request": request}
    )