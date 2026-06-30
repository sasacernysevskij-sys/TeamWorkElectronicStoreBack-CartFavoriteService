from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import engine, Base

from models.cart_item import CartItem
from models.favorite import Favorite

from routes.cart_routes import router as cart_router
from routes.favorite_routes import router as favorite_router


app = FastAPI(title="Cart Favorite Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(cart_router)
app.include_router(favorite_router)


@app.get("/")
def home():
    return {
        "message": "Cart Favorite Service работает!"
    }