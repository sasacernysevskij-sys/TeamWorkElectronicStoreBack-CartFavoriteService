from sqlalchemy import Column, Integer, UniqueConstraint
from db import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)#------------Уникальный идентификатор записи
    user_id = Column(Integer, nullable=False, index=True)#---------ID пользователя(нельзя для незарегистрированых)
    product_id = Column(Integer, nullable=False, index=True)#------ID товара

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_favorite_user_product"),
        # Один пользователь не может добавить товар в избранное дважды
    )