from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import Form


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
    
    @classmethod
    def as_form(
        cls,
         project_name:str = Form(...),
         start_date:str = Form(...),
         end_date:str = Form(...),
         description:str = Form(...),
         employee_id:str = Form(...)
        
    ):
        return cls(
            project_name=project_name,
            start_date=start_date,
            end_date=end_date,
            description=description,
            employee_id=employee_id
            
        )


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    
    
    @classmethod
    def as_form(
        cls,
         project_name:str = Form(...),
         start_date:str = Form(...),
         end_date:str = Form(...),
         description:str = Form(...),
        
    ):
        return cls(
            project_name=project_name,
            start_date=start_date,
            end_date=end_date,
            description=description,
            
        )


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