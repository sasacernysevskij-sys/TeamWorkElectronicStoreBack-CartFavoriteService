from models.cart_item import CartItem
from services.product_client import get_product


class CartService:
    def add_to_cart(self, db, user_id, product_id, quantity):
        if quantity <= 0:
            return {
                "detail": "Количество товара должно быть больше 0"
            }, 400

        product, product_status = get_product(product_id)

        if product_status == 404:
            return {
                "detail": "Товар не найден"
            }, 404

        if product_status != 200:
            return {
                "detail": "Не удалось получить товар из ProductService",
                "product_service_response": product
            }, product_status

        if product.get("stock", 0) < quantity:
            return {
                "detail": "Недостаточно товара на складе"
            }, 400

        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            )
            .first()
        )

        if cart_item is not None:
            new_quantity = cart_item.quantity + quantity

            if product.get("stock", 0) < new_quantity:
                return {
                    "detail": "Недостаточно товара на складе"
                }, 400

            cart_item.quantity = new_quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )

            db.add(cart_item)

        db.commit()
        db.refresh(cart_item)

        return {
            "id": cart_item.id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "product": {
                "id": product.get("id"),
                "name": product.get("name"),
                "price": product.get("price"),
                "stock": product.get("stock")
            }
        }, 201

    def get_cart(self, db, user_id):
        cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

        items = []
        total_price = 0

        for cart_item in cart_items:
            product, product_status = get_product(cart_item.product_id)

            if product_status != 200:
                continue

            subtotal = product.get("price", 0) * cart_item.quantity
            total_price += subtotal

            items.append({
                "cart_item_id": cart_item.id,
                "product_id": product.get("id"),
                "name": product.get("name"),
                "article": product.get("article"),
                "description": product.get("description"),
                "price": product.get("price"),
                "product_type": product.get("product_type"),
                "stock": product.get("stock"),
                "quantity": cart_item.quantity,
                "subtotal": subtotal,
                "image_url": product.get("image_url")
            })

        return {
            "items": items,
            "total_price": total_price
        }, 200

    def clear_cart(self, db, user_id):
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()

        return {
            "message": "Корзина очищена"
        }, 200

    def update_cart_item(self, db, user_id, product_id, quantity):
        if quantity <= 0:
            return {
                "detail": "Количество товара должно быть больше 0"
            }, 400

        product, product_status = get_product(product_id)

        if product_status == 404:
            return {
                "detail": "Товар не найден"
            }, 404

        if product_status != 200:
            return {
                "detail": "Не удалось получить товар из ProductService",
                "product_service_response": product
            }, product_status

        if product.get("stock", 0) < quantity:
            return {
                "detail": "Недостаточно товара на складе"
            }, 400

        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            )
            .first()
        )

        if cart_item is None:
            return {
                "detail": "Товар не найден в корзине"
            }, 404

        cart_item.quantity = quantity

        db.commit()
        db.refresh(cart_item)

        return {
            "id": cart_item.id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity
        }, 200

    def remove_cart_item(self, db, user_id, product_id):
        cart_item = (
            db.query(CartItem)
            .filter(
                CartItem.user_id == user_id,
                CartItem.product_id == product_id
            )
            .first()
        )

        if cart_item is None:
            return {
                "detail": "Товар не найден в корзине"
            }, 404

        db.delete(cart_item)
        db.commit()

        return {
            "detail": "Товар удалён из корзины"
        }, 200