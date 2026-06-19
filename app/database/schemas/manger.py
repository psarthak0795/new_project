from pydantic import BaseModel, EmailStr


class UserMini(BaseModel):
    id: int
    first_name: str
    email: EmailStr

    class Config:
        from_attributes = True
        
class ProjectWithManager(BaseModel):
    id: int
    project_name: str
    start_date: str
    end_date: str
    description: str
    manager: UserMini

    class Config:
        from_attributes = True