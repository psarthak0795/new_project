from pydantic import BaseModel
from typing import Optional
from datetime import date


class ProjectBase(BaseModel):
    project_name: str
    start_date: date
    end_date: date
    description: str

# class ProjectCreate(BaseModel):
#     project_name: str
#     start_date: str
#     end_date: str
#     description: str


class ProjectCreate(ProjectBase):
    project_name: Optional[str] = None
    start_date: Optional[date] = None    
    end_date: Optional[date] = None
    description: Optional[str] = None
    employee_id: Optional[int] = None


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    
    id:int
    project_name:str
    start_date:date
    end_date:date
    description:str
    employee_id: int
    created_by: int
    manager_name:str
    employee_name:str
    
    
    

    
    

    class Config:
        from_attributes = True