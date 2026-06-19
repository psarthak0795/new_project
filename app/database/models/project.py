from app.database.connection import Base
from app.database.models.user import UserRole
from sqlalchemy import Column, Integer, String, ForeignKey, func , DateTime,Date
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
   
    
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_projects")
    employee = relationship("User", foreign_keys=[employee_id], back_populates="assigned_projects")
    
    @property
    def manager_name(self):
        if self.creator:
            return f"{self.creator.first_name} {self.creator.last_name}"
        return ""
    
    @property
    def employee_name(self):
        if self.employee:
            return f"{self.employee.first_name} {self.employee.last_name}"
        return ""

