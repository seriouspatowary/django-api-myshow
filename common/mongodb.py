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

def get_casts_collection():
    return db["casts"]

def get_crew_collection():
    return db["crews"]

def get_theatre_collection():
      return db["theatres"]
  
def get_screen_collection():
    return db["screens"]

def get_shows_collection():
    return db["shows"]

def get_seat_collection():
    return db["seats"]
      
      
def get_booking_collection():
    return db["bookings"]
def get_seat_locks_collection():
    return db["seatlocks"]