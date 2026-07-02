from sqlalchemy import or_
from sqlalchemy.orm import Session,aliased
from fastapi import HTTPException , Depends
from app.database.schemas import project
from app.dependencies.auth import get_current_user

from app.database.models.project import Project
from app.database.models.user import User, UserRole
from app.database.schemas.project import ProjectCreate, ProjectUpdate


def manager_required(
    current_user=Depends(get_current_user)
):
    if current_user.role != UserRole.manager:
        raise HTTPException(
            status_code=403,
            detail="Only managers can manage projects"
        )

    return current_user


def create_project(db: Session, project_data: ProjectCreate,current_user_id:int):
    new_project = Project(project_name=project_data.project_name,
                          start_date=project_data.start_date, end_date=project_data.end_date, 
                          description=project_data.description, created_by=current_user_id,
                          employee_id=project_data.employee_id)

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects_by_creator_id(db: Session,creator_id: int):
    return (db.query(Project).filter(Project.created_by == creator_id).all())


def update_project(db: Session, project: Project, data: dict):
    # Ensure we never overwrite required project relations with null values.
    if "employee_id" in data and data["employee_id"] is None:
        data.pop("employee_id")

    for key, value in data.items():
        if value is not None:
            setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project):
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}


def create_project_for_current_user(
    db: Session,
    project: ProjectCreate,
    current_user_id:int):
    return create_project(
        db,
        project,
       current_user_id)
    

def update_project_for_current_user(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate):

    project = get_project_by_id(db, project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    
    return update_project(
        db=db,
        project=project,
        data=project_data.model_dump(exclude_unset=True, exclude_none=True)
    )

def delete_project_for_current_user(
    db: Session,
    project_id: int,
    current_user_id: int
):
   
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

   

    return delete_project(db=db, project=project)

def get_team_view_service(db: Session, user_id: int):
    
    Manager = aliased(User)
    Employee = aliased(User)
    
    teams = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
             
                Manager.id.label("manager_id"),
                Manager.first_name.label("manager_first_name"),
                Manager.last_name.label("manager_last_name"),
                Manager.designation.label("manager_designation"),
                
                Employee.id.label("emp_id"),
                Employee.first_name.label("emp_first_name"),
                Employee.last_name.label("emp_last_name"),
                Employee.designation.label("emp_designation")        
        )
        .join(Manager, Project.created_by == Manager.id)
        .join(Employee, Project.employee_id == Employee.id)
        .filter(
            or_(
                Project.created_by == user_id,
                Project.employee_id == user_id
            )
        )
        .all()
    )
    
    return teams