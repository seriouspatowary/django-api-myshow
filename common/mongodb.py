from dotenv import load_dotenv

load_dotenv()
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client.get_default_database()


def get_users_collection():
    return db["users"]

def get_movies_collection():
    return db["movies"]