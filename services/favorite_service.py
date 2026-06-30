from models.favorite import Favorite
from services.product_client import get_product


class FavoriteService:
    def add_to_favorites(self, db, user_id, product_id):
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

        existing = (
            db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.product_id == product_id
            )
            .first()
        )

        if existing:
            return {
                "detail": "Товар уже в избранном"
            }, 400

        favorite = Favorite(
            user_id=user_id,
            product_id=product_id
        )

        db.add(favorite)
        db.commit()
        db.refresh(favorite)

        return {
            "id": favorite.id,
            "user_id": favorite.user_id,
            "product_id": favorite.product_id
        }, 201

    def get_favorites(self, db, user_id):
        favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()

        items = []

        for fav in favorites:
            product, product_status = get_product(fav.product_id)

            if product_status != 200:
                continue

            items.append({
                "favorite_id": fav.id,
                "product_id": product.get("id"),
                "name": product.get("name"),
                "price": product.get("price"),
                "image_url": product.get("image_url"),
                "rating": product.get("rating"),
                "product_type": product.get("product_type"),
                "stock": product.get("stock"),
                "article": product.get("article"),
                "description": product.get("description")
            })

        return {
            "items": items
        }, 200

    def remove_from_favorites(self, db, user_id, product_id):
        favorite = (
            db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.product_id == product_id
            )
            .first()
        )

        if favorite is None:
            return {
                "detail": "Товар не найден в избранном"
            }, 404

        db.delete(favorite)
        db.commit()

        return {
            "detail": "Товар удалён из избранного"
        }, 200

    def clear_favorites(self, db, user_id):
        db.query(Favorite).filter(Favorite.user_id == user_id).delete()
        db.commit()

        return {
            "detail": "Все товары удалены из избранного"
        }, 200