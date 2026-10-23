
import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, serverSelectionTimeoutMS=10000)

try:
    client.admin.command("ping")
    db = client["electronics_catalog"]
    products = db["products"]

    print("\n=== 1. Все товары ===")
    for item in products.find({}, {"_id": 0, "name": 1, "price": 1}).limit(5):
        print(item)

    print("\n=== 2. Поиск смартфонов ===")
    for item in products.find({"category": "Смартфоны"}, {"_id": 0, "name": 1}):
        print(item)

    print("\n=== 3. Товары Apple ===")
    for item in products.find({"brand": "Apple"}, {"_id": 0, "name": 1, "price": 1}):
        print(item)

    print("\n=== 4. Товары дешевле 100 000 тенге ===")
    for item in products.find({"price": {"$lt": 100000}}, {"_id": 0, "name": 1, "price": 1}):
        print(item)

    print("\n=== 5. Товары стоимостью от 100 000 до 300 000 тенге ===")
    for item in products.find(
        {"price": {"$gte": 100000, "$lte": 300000}},
        {"_id": 0, "name": 1, "price": 1}
    ).sort("price", ASCENDING):
        print(item)

    print("\n=== 6. Товары в наличии с остатком не менее 10 ===")
    for item in products.find(
        {"stock": {"$gte": 10}},
        {"_id": 0, "name": 1, "stock": 1}
    ).sort("stock", DESCENDING):
        print(item)

    print("\n=== 7. Сложный запрос: Apple дороже 200 000 тенге ===")
    for item in products.find(
        {"brand": "Apple", "price": {"$gt": 200000}},
        {"_id": 0, "name": 1, "price": 1}
    ).sort("price", DESCENDING):
        print(item)

    print("\n=== 8. Количество и средняя цена по категориям ===")
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1},
                "average_price": {"$avg": "$price"}
            }
        },
        {"$sort": {"average_price": -1}}
    ]

    for item in products.aggregate(pipeline):
        print({
            "category": item["_id"],
            "count": item["count"],
            "average_price": round(item["average_price"], 2)
        })

    print("\n=== Создание индексов ===")
    products.create_index([("category", ASCENDING), ("price", ASCENDING)])
    products.create_index([("brand", ASCENDING), ("price", ASCENDING)])
    products.create_index([("name", TEXT)])
    print("Индексы созданы.")

    print("\n=== Проверка индексов ===")
    print(products.index_information())

except Exception as error:
    print("Ошибка:", type(error).__name__, str(error))

finally:
    client.close()
