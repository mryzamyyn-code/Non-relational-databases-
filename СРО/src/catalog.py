import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("Не найдена переменная MONGODB_URI в файле .env")

client = MongoClient(MONGODB_URI)
db = client["electronics_catalog"]
products = db["products"]


def create_product(name, category, brand, price, stock):
    """Добавить новый товар."""
    product = {
        "name": name,
        "category": category,
        "brand": brand,
        "price": float(price),
        "stock": int(stock)
    }
    result = products.insert_one(product)
    return str(result.inserted_id)


def get_products(limit=100):
    """Получить список товаров."""
    return list(products.find().limit(limit))


def get_product_by_id(product_id):
    """Найти товар по ID."""
    if not ObjectId.is_valid(product_id):
        return None

    return products.find_one({"_id": ObjectId(product_id)})


def update_product(product_id, updates):
    """Изменить данные товара."""
    if not ObjectId.is_valid(product_id):
        return False

    allowed_fields = {"name", "category", "brand", "price", "stock"}
    clean_updates = {
        key: value
        for key, value in updates.items()
        if key in allowed_fields
    }

    if not clean_updates:
        return False

    if "price" in clean_updates:
        clean_updates["price"] = float(clean_updates["price"])

    if "stock" in clean_updates:
        clean_updates["stock"] = int(clean_updates["stock"])

    result = products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": clean_updates}
    )
    return result.modified_count > 0


def delete_product(product_id):
    """Удалить товар по ID."""
    if not ObjectId.is_valid(product_id):
        return False

    result = products.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0


if __name__ == "__main__":
    print("CRUD-модуль подключён к MongoDB.")
    print("Количество товаров:", products.count_documents({}))
    client.close()