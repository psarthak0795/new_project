from fastapi import APIRouter

from app.services.refresh import refresh_access_token

router = APIRouter(tags=["Refresh"])


@router.post("/refresh")
def refresh_token(token: str):
    return refresh_access_token(token)
