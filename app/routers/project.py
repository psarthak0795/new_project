from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.database.models.user import User
from app.database.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project import delete_project_for_current_user, create_project_for_current_user, update_project_for_current_user, manager_required
from app.services.manager import get_projects


router = APIRouter(tags=["Project"])

@router.post("/projects", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(manager_required)
):
    return create_project_for_current_user(db,project,current_user.id)

# @router.get("/projects",response_model=list[ProjectResponse])
# def get_projects(
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)):
   
#     return get_projects(
#         db,current_user.id)
    
@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(manager_required)):
    return update_project_for_current_user(
        db,project_id,project,current_user.id)
    
@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,db: Session = Depends(get_db),
    current_user=Depends(manager_required)):
    return delete_project_for_current_user(
        db,project_id,current_user.id)
    
    