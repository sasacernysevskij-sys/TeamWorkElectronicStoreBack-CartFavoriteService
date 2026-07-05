import requests
from concurrent.futures import ThreadPoolExecutor
from config import PRODUCT_SERVICE_URL

# ---HTTP-клиент для общения с ProductService.
# ---Получает товар по ID через REST API.
# ---Возвращает кортеж (данные, статус-код)
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

# ---Получает несколько товаров параллельно через ThreadPoolExecutor.
# ---Быстрее чем последовательные запросы — используется в корзине
def get_products_batch(product_ids: list):
    if not product_ids:
        return {}

    def fetch_one(pid):
        product, status = get_product(pid)
        return (pid, product) if status == 200 else None

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_one, product_ids)

    return {pid: product for pid, product in results if product is not None}