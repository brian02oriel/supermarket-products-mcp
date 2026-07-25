from enum import Enum

from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING

class RETAILER_CODE(str, Enum):
    SUPERMERCADOS_REY = "SR"
    RIBA_SMITH = "RS"
    SUPER_XTRA = "SX"

class Product(BaseModel):
    retailer: str
    retailer_code: RETAILER_CODE
    category: str | None = None
    sub_category: str | None = None
    brand: str | None = None
    sku: str | None = None
    name: str | None = None
    price: float | None = None
    undiscounted_price: float | None = None
    currency: str | None = None
    size: str | None = None
    url: str | None = None
    image_url: str | None = None

class ProductFilter(BaseModel):
    retailer_code: list[RETAILER_CODE] | None = None
    category: list[str] | None = None
    sub_category: list[str] | None = None
    brand: list[str] | None = None
    from_undiscounted_price: float | None = None
    to_undiscounted_price: float | None = None
    from_price: float | None = None
    to_price: float | None = None
    def to_filter(self) -> dict:
        f = {}
        if self.retailer_code:
            f["retailer_code"] = {"$in": self.retailer_code}
        if self.category:
            f["category"] = {"$in": self.category}
        if self.sub_category:
            f["sub_category"] = {"$in": self.sub_category}
        if self.brand:
            f["brand"] = {"$in": self.brand}
        if self.from_undiscounted_price is not None:
            f["undiscounted_price"] = {**f.get("undiscounted_price", {}), "$gte": self.from_undiscounted_price}
        if self.to_undiscounted_price is not None:
            f["undiscounted_price"] = {**f.get("undiscounted_price", {}), "$lte": self.to_undiscounted_price}
        if self.from_price is not None:
            f["price"] = {**f.get("price", {}), "$gte": self.from_price}
        if self.to_price is not None:
            f["price"] = {**f.get("price", {}), "$lte": self.to_price}
        return f

class SortField(str, Enum):
    BRAND = "brand"
    CATEGORY = "category"
    SUB_CATEGORY = "sub_category"
    PRICE = "price"
    UNDISCOUNTED_PRICE = "undiscounted_price"
    NAME = "name"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class ProductSort(BaseModel):
    field: SortField
    order: SortOrder = SortOrder.ASC

class ProductSortOptions(BaseModel):
    sorts: list[ProductSort] = []

    def to_sort(self) -> list[tuple[str, int]]:
        return [
            (s.field.value, ASCENDING if s.order == SortOrder.ASC else DESCENDING)
            for s in self.sorts
        ] 