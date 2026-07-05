# Cart-Favorite Service — сервис корзины и избранного

## Описание
Микросервис отвечает за управление корзиной покупок и списком избранных товаров пользователя

## Пакеты
- Python 
- FastAPI 
- SQLAlchemy
- PyJWT 
- Pydantic 
- Requests (HTTP-клиенты к AuthService и ProductService)

### Локально/запуск
pip install -r requirements.txt
uvicorn app:app --reload --port 8003

### Docker/запуск
docker build -t cart-favorite-service .
docker run -d -p 8003:8003 --name cart-container cart-favorite-service

### Docker Compose (все сервисы)/запуск
docker-compose up -d --build

## Переменные окружения (.env)
SECRET_KEY=ваш-секретный-ключ
AUTH_SERVICE_URL=http://auth:8001
PRODUCT_SERVICE_URL=http://product:8002

## API

### Корзина

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | /api/cart | Содержимое корзины | Авторизован |
| POST | /api/cart/items | Добавить товар | Авторизован |
| PUT | /api/cart/items/{id} | Изменить количество | Авторизован |
| DELETE | /api/cart/items/{id} | Удалить товар | Авторизован |
| DELETE | /api/cart | Очистить корзину | Авторизован |
| DELETE | /api/cart/clear | Очистить корзину (для OrderService) | OrderService |

### Избранное

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | /api/favorites | Список избранного | Авторизован |
| POST | /api/favorites | Добавить в избранное | Авторизован |
| DELETE | /api/favorites/{id} | Удалить из избранного | Авторизован |
| DELETE | /api/favorites | Очистить избранное | Авторизован |

## URL
http://localhost:8003/docs