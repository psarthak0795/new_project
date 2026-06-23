from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import Form


class UserRole(str, Enum):
    manager = "manager"
    employee = "employee"


class GenderType(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr | None = None
    phone: str
    
    role: UserRole
    gender: GenderType
    
    designation: str
    joining_date: date
    address: str
    zip_code: str
    city: str
    state: str
    country: str
    dob: date
    password: str

    @classmethod
    def as_form(
        cls,
        first_name:str = Form(...),
    middle_name:str = Form(...),
        last_name:str = Form(...),
    email:str = Form(...),
        phone:str = Form(...),
        role:str = Form(...),
        gender:str = Form(...),
    designation:str = Form(...),
        joining_date:str = Form(...),
    address:str = Form(...),
        zip_code:str = Form(...),
        city:str = Form(...),
        state:str = Form(...),
        country:str = Form(...),
        dob:str = Form(...),
        password:str = Form(...)
    ):
        return cls(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=role,
            gender=gender,
            designation=designation,
            joining_date=joining_date,
            address=address,
            zip_code=zip_code,
            city=city,
            state=state,
            country=country,
            dob=dob,
            password=password)
    


   

            
        

class UserResponse(BaseModel):
    id: int
    first_name: str
    middle_name: str 
    last_name: str
    email: str 
    phone: str
    
    role: UserRole
    gender: GenderType
    
    designation: str
    joining_date: str
    address: str
    zip_code: str
    city: str
    state: str
    country: str
    dob: str
    password: str

    class Config:
        from_attributes = True