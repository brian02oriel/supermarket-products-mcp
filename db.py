# db.py
from pymongo import AsyncMongoClient

from repositories.products.repository import ProductRepository

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "genie"

mongo_client = AsyncMongoClient(MONGO_URI)
product_repo = ProductRepository(mongo_client[DB_NAME]["products"])