from sqlalchemy import Column, Integer, UniqueConstraint
from db import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)#------------Уникальный идентификатор записи
    user_id = Column(Integer, nullable=False, index=True)#---------ID пользователя(нельзя для незарегистрированых)
    product_id = Column(Integer, nullable=False, index=True)#------ID товара
    quantity = Column(Integer, nullable=False)#--------------------Количество товара в корзине

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_cart_user_product"),
        # Один пользователь не может добавить один товар дважды — увеличивается quantity
    )