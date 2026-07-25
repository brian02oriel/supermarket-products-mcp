import csv
import os
from pathlib import Path

from pymongo import MongoClient, UpdateOne

from repositories.products.model import RETAILER_CODE, Product

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "genie"
COLLECTION_NAME = "products"
RETAILER_CODES = {
    "Supermercados Rey": RETAILER_CODE.SUPERMERCADOS_REY,
    "Riba Smith": RETAILER_CODE.RIBA_SMITH,
    "Super Xtra": RETAILER_CODE.SUPER_XTRA
}

    
def parse_row(row: dict) -> Product:
    return Product(
        retailer=row["Retailer"] or None,
        retailer_code=RETAILER_CODES.get(row["Retailer"]) or None,
        category=row["Category"] or None,
        sub_category=row["SubCategory"] or None,
        brand=row["Brand"] or None,
        sku=row["SKU"] or None,
        name=row["Name"] or None,
        price=float(row["Price"]) if row["Price"] else None,
        undiscounted_price=float(row["UndiscountedPrice"]) if row["UndiscountedPrice"] else None,
        currency=row["Currency"] or None,
        size=row["Size"] or None,
        url=row["Url"] or None,
        image_url=row["ImageUrl"] or None,
    )


def load_csv(path: Path) -> list[Product]:
    with path.open(newline="", encoding="utf-8") as f:
        return [parse_row(row) for row in csv.DictReader(f)]


def main() -> None:
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]
    
    # Creates a MongoDB compound index on the collection, each ascending (1 = ascending order)
    # This speeds up queries/lookups that filter or sort by those fields together
    collection.create_index([("retailer", 1), ("retailer_code", 1), ("sku", 1)])

    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}")
        return

    total = 0
    for csv_file in csv_files:
        documents = load_csv(csv_file)
        if not documents:
            continue

        operations = [
            UpdateOne(
                {"retailer_code": doc.retailer_code, "sku": doc.sku},
                {"$set": doc.model_dump(mode="json")},
                upsert=True,
            )
            for doc in documents
        ]
        collection.bulk_write(operations, ordered=False)
        total += len(documents)
        print(f"Loaded {len(documents)} products from {csv_file.name}")

    print(f"Done. Upserted {total} products into {DB_NAME}.{COLLECTION_NAME}")


if __name__ == "__main__":
    main()