# db.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.collection import AsyncCollection

from repositories.products.repository import ProductRepository

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "genie"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create client once, store on app.state
    app.state.mongo_client = AsyncMongoClient(MONGO_URI)
    yield
    # Shutdown: close the client cleanly
    await app.state.mongo_client.close()


def get_db(request: Request) -> AsyncDatabase:
    return request.app.state.mongo_client[DB_NAME]


def get_product_collection(db: AsyncDatabase = Depends(get_db)) -> AsyncCollection:
    return db["products"]


def get_product_repo(collection: AsyncCollection = Depends(get_product_collection)) -> ProductRepository:
    return ProductRepository(collection)