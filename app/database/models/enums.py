from enum import Enum


class UserRole(str, Enum):
    manager = "manager"
    employee = "employee"


class GenderType(str, Enum):
    male = "male"
    female = "female"
    other = "other"