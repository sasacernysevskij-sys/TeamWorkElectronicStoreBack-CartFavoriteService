from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.auth_client import get_current_user


security = HTTPBearer()


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return credentials.credentials


def get_current_user_from_auth(
    token: str = Depends(get_current_token)
):
    user = get_current_user(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен или истёк"
        )

    return user


def get_current_user_id(
    current_user: dict = Depends(get_current_user_from_auth)
):
    return current_user.get("id")