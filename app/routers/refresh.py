from fastapi import APIRouter, Request, Response, HTTPException

from app.services.refresh import refresh_access_token

router = APIRouter(tags=["Refresh"])


@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if token is None:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    refreshed = refresh_access_token(token)
    response.set_cookie(
        key="access_token",
        value=refreshed["access_token"],
        path="/",
        httponly=True,
        max_age=3600,
        samesite="lax"
    )
    return refreshed
