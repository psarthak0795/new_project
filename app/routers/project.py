from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.database.models.user import User
from app.database.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse ,TeamViewResponse
from app.services.project import delete_project_for_current_user, create_project_for_current_user, update_project_for_current_user, manager_required, get_project_by_id,get_team_view_service

templates = Jinja2Templates(directory="app/templates")



router = APIRouter(tags=["Project"])

@router.post("/projects")
def create_project(
    payload: ProjectCreate = Depends(ProjectCreate.as_form),
    db: Session = Depends(get_db),
    current_user=Depends(manager_required)
):
    
    create_project_for_current_user(db,payload,current_user.id)
    return RedirectResponse(
        url="/projects",
        status_code=303
    )

@router.get("/projects/edit/{project_id}", response_class=HTMLResponse)
def edit_project_page(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(manager_required)
):
    project = get_project_by_id(db, project_id)
    if not project:
        return RedirectResponse(url="/projects", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="updateproject.html",
        context={"request": request, "project": project}
    )

@router.post("/projects/update/{project_id}")
def submit_update_project(
    project_id: int,
    project_name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    description: str = Form(...),
    status: str = Form(None),
    db: Session = Depends(get_db),
    current_user=Depends(manager_required)
):
    project_data = ProjectUpdate(
        project_name=project_name,
        start_date=start_date,
        end_date=end_date,
        description=description
    )
    
    update_project_for_current_user(db, project_id, project_data)
    return RedirectResponse(url="/projects", status_code=303)


@router.post("/projects/delete/{project_id}")
def delete_project_post(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(manager_required)
):
    delete_project_for_current_user(db, project_id, current_user.id)
    return RedirectResponse(url="/projects", status_code=303)

# @router.get("/projects",response_model=list[ProjectResponse])
# def get_projects(
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)):
   
#     return get_projects(
#         db,current_user.id)
    
# @router.put("/projects/{project_id}", response_model=ProjectResponse)
# def update_project(
#     project_id: int,
#     project: ProjectUpdate,
#     db: Session = Depends(get_db),
#     current_user=Depends(manager_required)):
#     return update_project_for_current_user(
#         db,project_id,project,current_user.id)
    
# @router.delete("/projects/{project_id}")
# def delete_project(
#     project_id: int,db: Session = Depends(get_db),
#     current_user=Depends(manager_required)):
#     return delete_project_for_current_user(
#         db,project_id,current_user.id)

@router.get("/teamview", response_class=HTMLResponse)
def team_view(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    teams = [
        TeamViewResponse.model_validate(team)
        for team in get_team_view_service(db,current_user.id)
    ]
    
    response = templates.TemplateResponse(
        request=request,
        name= "teampage.html",
        context={
            "request" : request,
            "teams": teams,
            "user": current_user
        }
    )
    
    response.headers["Cache-Countrol"] = "no-store"
    
    return response