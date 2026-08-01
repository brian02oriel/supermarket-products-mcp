import argparse
import os
from pathlib import Path

from pymongo import MongoClient

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "genie"
COLLECTION_NAME = "products"

OUTPUT_FILENAMES = {
    "category": "categories.txt",
    "sub_category": "subcategories.txt",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export distinct values of a product field to a comma-separated .txt file.")
    parser.add_argument("field", choices=sorted(OUTPUT_FILENAMES))
    field = parser.parse_args().field

    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    values = collection.distinct(field)
    sorted_values = sorted(v for v in values if v is not None)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / OUTPUT_FILENAMES[field]
    output_path.write_text(",".join(sorted_values), encoding="utf-8")
    print(f"Wrote {len(sorted_values)} {field} values to {output_path}")


if __name__ == "__main__":
    main()
