from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.project import manager_required
from app.database.models.project import Project
from app.database.models.user import User, UserRole
from app.database.schemas.project import ProjectResponse

def get_all_projects(db: Session):
    return db.query(Project).all()






# def get_projects(db: Session, user_id: int):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user.role.value == "manager":
#         projects = db.query(Project).filter(Project.created_by == user_id).all()
#     else:
#         projects = db.query(Project).filter(Project.employee_id == user_id).all()
        
#     return [ProjectResponse(
#             id=project.id,
#             project_name=project.project_name,
#             start_date=project.start_date,
#             end_date=project.end_date,
#             description=project.description,
#             employee_id=project.employee_id,
#             created_by=project.created_by,
#             manager_name=(f"{project.creator.first_name} {project.creator.last_name}")
#             if project.creator else"",
#             employee_name=(f"{project.employee.first_name} {project.employee.last_name}")
#             if project.employee else""
#     )
#     for project in projects
# ]
    
def get_projects_by_manager(db: Session, manager_id: int):
    return (
        db.query(Project)
        .filter(Project.created_by == manager_id)
        .all()
    )


def get_projects_by_employee(db: Session, employee_id: int):
    return (
        db.query(Project)
        .filter(Project.employee_id == employee_id)
        .all()
    )