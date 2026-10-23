
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def test_mongodb_connection():
    uri = os.getenv("MONGODB_URI")
    assert uri, "Не найдена переменная MONGODB_URI в .env"

    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    try:
        result = client.admin.command("ping")
        assert result["ok"] == 1
    finally:
        client.close()


def test_catalog_has_30_demo_products():
    uri = os.getenv("MONGODB_URI")
    assert uri, "Не найдена переменная MONGODB_URI в .env"

    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    try:
        collection = client["electronics_catalog"]["products"]
        count = collection.count_documents({"seed_source": "sro_demo"})
        assert count == 30, f"Ожидалось 30 демонстрационных товаров, найдено: {count}"
    finally:
        client.close()


def test_products_have_required_fields():
    uri = os.getenv("MONGODB_URI")
    assert uri, "Не найдена переменная MONGODB_URI в .env"

    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    try:
        collection = client["electronics_catalog"]["products"]
        product = collection.find_one({"seed_source": "sro_demo"})
        assert product is not None
        assert product.get("name")
        assert product.get("category")
        assert product.get("brand")
        assert isinstance(product.get("price"), (int, float))
        assert isinstance(product.get("stock"), int)
    finally:
        client.close()


from src.catalog import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product,
)


def test_crud_operations():
    product_id = create_product(
        name="Тестовый товар CRUD",
        category="Тест",
        brand="TestBrand",
        price=1000,
        stock=5,
    )

    try:
        # READ: найти созданный товар
        product = get_product_by_id(product_id)
        assert product is not None
        assert product["name"] == "Тестовый товар CRUD"

        # READ: получить список товаров
        assert len(get_products()) >= 1

        # UPDATE: изменить цену
        updated = update_product(product_id, {"price": 1500})
        assert updated is True

        product = get_product_by_id(product_id)
        assert product["price"] == 1500.0

    finally:
        # DELETE: удалить только созданный тестовый товар
        assert delete_product(product_id) is True

    assert get_product_by_id(product_id) is None


