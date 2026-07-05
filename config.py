import os

# Секретный ключ для JWT (должен совпадать с AuthService для расшифровки токенов)
SECRET_KEY = os.getenv("SECRET_KEY", "auth-secret-key-123")

# URL базы данных (по умолчанию SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cart_favorites.db")

# Время жизни JWT-токена в часах
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# URL сервиса авторизации (для проверки токенов)
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth:8001")

# URL сервиса товаров (для получения информации о товарах)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product:8002")