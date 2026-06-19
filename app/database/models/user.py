from app.database.connection import Base
from sqlalchemy import Column, Date, Integer, String, Enum, func , DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    manager = "manager"
    employee = "employee"


class GenderType(str, PyEnum):
    male = "male"
    female = "female"
    other = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)

    role = Column(Enum(UserRole, name="user_role_enum"),nullable=False)

    gender = Column(Enum(GenderType, name="gender_type_enum"),nullable=False)

    designation = Column(String, nullable=False)
    password = Column(String, nullable=False)

    joining_date = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    dob = Column(Date, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    created_projects = relationship("Project", foreign_keys="[Project.created_by]", back_populates="creator")
    assigned_projects = relationship("Project", foreign_keys="[Project.employee_id]", back_populates="employee")