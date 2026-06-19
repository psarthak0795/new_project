from datetime import date
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRole(str, Enum):
    manager = "manager"
    employee = "employee"


class GenderType(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserBase(BaseModel):
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


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True