from pymongo.asynchronous.collection import AsyncCollection
from bson import ObjectId

from repositories.products.model import ProductFilter, ProductSortOptions

class ProductRepository:
    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def drop_indexes(self):
        await self.collection.drop_indexes()

    async def ensure_indexes(self):
        await self.collection.create_index([
            ("retailer", "text"),
            ("name", "text"),
            ("brand", "text"),
            ("category", "text"),
            ("sub_category", "text")
        ], name="text_index")
        
    async def get_product_by_id(self, product_id: str):
        product = await self.collection.find_one({"_id": ObjectId(product_id)})
        return product
    
    
    async def get_products(self, filter: ProductFilter | None = None, sort_by: ProductSortOptions | None = None, limit: int | None = None):
        sort = sort_by.to_sort() if sort_by else []
        cursor = self.collection.find(filter.to_filter() if filter else {})
        if sort:
            cursor = cursor.sort(sort)
        if limit is not None:
            cursor = cursor.limit(limit)
        products = await cursor.to_list(length=None)
        return products
    
    async def get_products_count(self, filter: ProductFilter | None = None):
        count = await self.collection.count_documents(filter.to_filter() if filter else {})
        return count
    