from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db import get_db
from middleware.auth_middleware import get_current_user_id
from services.favorite_service import FavoriteService


router = APIRouter(prefix="/api/favorites", tags=["favorites"])

favorite_service = FavoriteService()

class FavoriteRequest(BaseModel):
    product_id: int

# ---Добавляет товар в избранное. Требует авторизации (Bearer токен)
@router.post("")
def add_to_favorites(
    data: FavoriteRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = favorite_service.add_to_favorites(
        db=db,
        user_id=current_user_id,
        product_id=data.product_id
    )

    return JSONResponse(status_code=status_code, content=result)

# ---Возвращает список избранных товаров пользователя с актуальными ценами
@router.get("")
def get_favorites(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = favorite_service.get_favorites(
        db=db,
        user_id=current_user_id
    )

    return JSONResponse(status_code=status_code, content=result)

# ---Удаляет один товар из избранного по ID товара
@router.delete("/{product_id}")
def remove_from_favorites(
    product_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = favorite_service.remove_from_favorites(
        db=db,
        user_id=current_user_id,
        product_id=product_id
    )

    return JSONResponse(status_code=status_code, content=result)

# ---Удаляет все товары из избранного пользователя
@router.delete("")
def clear_favorites(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    result, status_code = favorite_service.clear_favorites(
        db=db,
        user_id=current_user_id
    )

    return JSONResponse(status_code=status_code, content=result)