from pydantic import BaseModel, EmailStr
from fastapi import Form

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    @classmethod
    def as_form(
        cls,
        email:str = Form(...),
        password:str = Form(...)
    ):
        return cls(
            email=email,
            password=password
        )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str