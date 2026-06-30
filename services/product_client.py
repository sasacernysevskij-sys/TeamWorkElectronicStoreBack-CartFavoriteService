import requests

from config import PRODUCT_SERVICE_URL


def get_product(product_id: int):
    try:
        response = requests.get(
            f"{PRODUCT_SERVICE_URL}/api/products/{product_id}",
            timeout=5
        )

        try:
            data = response.json()
        except ValueError:
            data = {"detail": "Некорректный ответ ProductService"}

        return data, response.status_code

    except requests.RequestException:
        return {"detail": "ProductService недоступен"}, 503