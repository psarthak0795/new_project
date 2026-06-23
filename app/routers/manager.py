from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.database.models.user import User
from app.database.schemas.project import ProjectResponse
from app.services.manager import get_projects_by_employee,get_projects_by_manager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Project"])


@router.get("/projects/create", response_class=HTMLResponse)
def create_project_page(request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        request=request,
        name="createproject.html",
        context={
            "request": request,
            "user": current_user
        }
    )


# @router.get("/projects",response_model=list[ProjectResponse])
# def get_my_projects(db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)):
#     print("Current user id:", current_user.id)

#     return get_projects(db, current_user.id)

@router.get("/projects",  response_class=HTMLResponse)
def get_my_projects(request:Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    if current_user.role.value == "manager":
        # Return projects created by this manager
        projects = get_projects_by_manager(db, current_user.id)
    else:
        # Return projects assigned to this employee
        projects = get_projects_by_employee(db, current_user.id)
    for p in projects:
        print(
            "PROJECT:",
            p.employee_name
        )
    response = templates.TemplateResponse(
        request=request,
        name="projectpage.html",
        context={
            "request": request,
            "user" : current_user,
            "projects" : projects
        }
        
    )
    return response
