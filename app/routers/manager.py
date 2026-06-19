from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.database.models.user import User
from app.database.schemas.project import ProjectResponse
from app.services.manager import get_projects

router = APIRouter(tags=["Project"])


@router.get("/projects",response_model=list[ProjectResponse])
def get_my_projects(db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    print("Current user id:", current_user.id)

    return get_projects(db, current_user.id)


