from mcp_instance import mcp
from repositories.products.model import RETAILER_CODE


@mcp.tool()
def get_products(
    retailer_code: list[RETAILER_CODE] | None = None,
    category: list[str] | None = None,
    sub_category: list[str] | None = None,
    brand: list[str] | None = None,
) -> dict:
    """Search supermarket products, optionally filtered by retailer, category, sub-category, and/or brand."""
    # TODO: delegate to repositories.products.repository once it queries MongoDB
    return {
        "retailer_code": retailer_code,
        "category": category,
        "sub_category": sub_category,
        "brand": brand,
    }
