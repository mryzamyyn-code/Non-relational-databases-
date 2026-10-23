import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
database_name = os.getenv("MONGODB_DATABASE")

if not uri:
    raise ValueError("Не найдена строка подключения в .env")

client = MongoClient(uri, serverSelectionTimeoutMS=10000)

try:
    client.admin.command("ping")
    print("Успешное подключение к MongoDB!")

    db = client[database_name]
    print("База данных:", db.name)

except Exception as error:
    print("Ошибка подключения:", str(error))

finally:
    client.close()