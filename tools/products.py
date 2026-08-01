from db import product_repo
from mcp_instance import mcp
from repositories.products.model import RETAILER_CODE, Product, ProductFilter, ProductSort, ProductSortOptions


@mcp.tool()
# Change with pydantic models whenever the bug in the inspector is fixed
async def get_products(
    search: str | None = None,
    retailer_code: list[RETAILER_CODE] | None = None,
    category: list[str] | None = None,
    sub_category: list[str] | None = None,
    brand: list[str] | None = None,
    undiscounted_price: float | None = None,
    price: float | None = None,
    sort_by: ProductSortOptions | None = None,
    limit: int | None = None
) -> list[Product]:
    """Search supermarket products, optionally filtered by retailer, category, sub-category, and/or brand."""
    
    filter = ProductFilter(
        search=search,
        retailer_code=retailer_code,
        category=category,
        sub_category=sub_category,
        brand=brand,
        undiscounted_price=undiscounted_price,
        price=price
    )

    products = await product_repo.get_products(filter, sort_by, limit)
    return products

@mcp.tool()
# Change with pydantic models whenever the bug in the inspector is fixed
async def get_products_count(
    search: str | None = None,
    retailer_code: list[RETAILER_CODE] | None = None,
    category: list[str] | None = None,
    sub_category: list[str] | None = None,
    brand: list[str] | None = None,
    undiscounted_price: float | None = None,
    price: float | None = None
) -> int:
    """Get the count of supermarket products, optionally filtered by retailer, category, sub-category, and/or brand."""
    
    filter = ProductFilter(
        search=search,
        retailer_code=retailer_code,
        category=category,
        sub_category=sub_category,
        brand=brand,
        undiscounted_price=undiscounted_price,
        price=price
    )

    count = await product_repo.get_products_count(filter)
    return count