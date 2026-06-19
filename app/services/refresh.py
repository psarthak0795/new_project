from fastapi import HTTPException
from jose import JWTError, jwt

from app.core.security import create_access_token, SECRET_KEY, ALGORITHM


def decode_refresh_token(token: str):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )


def refresh_access_token(token: str):
    try:
        payload = decode_refresh_token(token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        email = payload.get("sub")

        new_access_token = create_access_token(
            data={"sub": email}
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )