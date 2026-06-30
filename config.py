import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cart_favorites.db")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002")