
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("Не найдена переменная MONGODB_URI в файле .env")

products = [
    {"name": "iPhone 16", "category": "Смартфоны", "brand": "Apple", "price": 399000, "stock": 12},
    {"name": "iPhone 15", "category": "Смартфоны", "brand": "Apple", "price": 319000, "stock": 8},
    {"name": "Samsung Galaxy S25", "category": "Смартфоны", "brand": "Samsung", "price": 429000, "stock": 10},
    {"name": "Samsung Galaxy A56", "category": "Смартфоны", "brand": "Samsung", "price": 189000, "stock": 15},
    {"name": "Xiaomi Redmi Note 14", "category": "Смартфоны", "brand": "Xiaomi", "price": 119000, "stock": 20},
    {"name": "Xiaomi 14T", "category": "Смартфоны", "brand": "Xiaomi", "price": 249000, "stock": 7},
    {"name": "MacBook Air M3", "category": "Ноутбуки", "brand": "Apple", "price": 499000, "stock": 5},
    {"name": "MacBook Pro M4", "category": "Ноутбуки", "brand": "Apple", "price": 899000, "stock": 3},
    {"name": "ASUS VivoBook 15", "category": "Ноутбуки", "brand": "ASUS", "price": 279000, "stock": 9},
    {"name": "Lenovo IdeaPad Slim 3", "category": "Ноутбуки", "brand": "Lenovo", "price": 239000, "stock": 11},
    {"name": "HP Pavilion 15", "category": "Ноутбуки", "brand": "HP", "price": 329000, "stock": 6},
    {"name": "Acer Aspire 5", "category": "Ноутбуки", "brand": "Acer", "price": 259000, "stock": 8},
    {"name": "AirPods Pro 2", "category": "Наушники", "brand": "Apple", "price": 129000, "stock": 14},
    {"name": "AirPods 4", "category": "Наушники", "brand": "Apple", "price": 79900, "stock": 18},
    {"name": "Galaxy Buds3 Pro", "category": "Наушники", "brand": "Samsung", "price": 99900, "stock": 10},
    {"name": "Sony WH-1000XM5", "category": "Наушники", "brand": "Sony", "price": 179000, "stock": 4},
    {"name": "JBL Tune 770NC", "category": "Наушники", "brand": "JBL", "price": 54900, "stock": 13},
    {"name": "Xiaomi Redmi Buds 5", "category": "Наушники", "brand": "Xiaomi", "price": 24900, "stock": 22},
    {"name": "iPad Air", "category": "Планшеты", "brand": "Apple", "price": 349000, "stock": 6},
    {"name": "iPad Pro", "category": "Планшеты", "brand": "Apple", "price": 599000, "stock": 3},
    {"name": "Samsung Galaxy Tab S10", "category": "Планшеты", "brand": "Samsung", "price": 389000, "stock": 5},
    {"name": "Xiaomi Pad 6", "category": "Планшеты", "brand": "Xiaomi", "price": 169000, "stock": 9},
    {"name": "Apple Watch Series 10", "category": "Часы", "brand": "Apple", "price": 219000, "stock": 7},
    {"name": "Samsung Galaxy Watch 7", "category": "Часы", "brand": "Samsung", "price": 149000, "stock": 8},
    {"name": "Xiaomi Smart Band 9", "category": "Часы", "brand": "Xiaomi", "price": 19900, "stock": 25},
    {"name": "Canon EOS R50", "category": "Камеры", "brand": "Canon", "price": 399000, "stock": 4},
    {"name": "Sony Alpha A6400", "category": "Камеры", "brand": "Sony", "price": 429000, "stock": 3},
    {"name": "Logitech MX Master 3S", "category": "Аксессуары", "brand": "Logitech", "price": 59900, "stock": 12},
    {"name": "Logitech G Pro X", "category": "Аксессуары", "brand": "Logitech", "price": 79900, "stock": 6},
    {"name": "Samsung T7 SSD 1TB", "category": "Накопители", "brand": "Samsung", "price": 69900, "stock": 16},
]

client = MongoClient(uri, serverSelectionTimeoutMS=10000)

try:
    client.admin.command("ping")
    db = client["electronics_catalog"]
    collection = db["products"]

    # Удаляем только предыдущие демонстрационные записи этого скрипта.
    collection.delete_many({"seed_source": "sro_demo"})

    for product in products:
        product["seed_source"] = "sro_demo"

    result = collection.insert_many(products)

    print("Подключение к MongoDB успешно!")
    print(f"Добавлено товаров: {len(result.inserted_ids)}")
    print(f"Всего товаров в коллекции: {collection.count_documents({})}")
    print("Коллекция: products")

except Exception as error:
    print("Ошибка:", type(error).__name__, str(error))

finally:
    client.close()
