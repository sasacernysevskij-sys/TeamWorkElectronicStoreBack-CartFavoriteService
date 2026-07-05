from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utils.jwt_utils import decode_token
#auth middlewhere

security = HTTPBearer()


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return credentials.credentials


def get_current_user_id(
    token: str = Depends(get_current_token)
):
    user_id = decode_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен или истёк"
        )

    return user_id