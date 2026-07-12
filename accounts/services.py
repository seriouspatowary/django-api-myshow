from common.mongodb import get_users_collection
from accounts.schemas import user_schema
from common.password import hash_password, check_password
from bson import ObjectId

from common.jwt import (
    generate_access_token,
    generate_refresh_token,
    verify_refresh_token
)




def refresh_access_token(refresh_token):
   
    payload =verify_refresh_token(refresh_token)

    users = get_users_collection()

    user = users.find_one({
          "_id": ObjectId(payload["userId"])

    })

    if not user:
        raise Exception("User not found")
    
    access_token = generate_access_token({
        "userId": str(user["_id"]),
        "role": user["role"]
    })

    user["_id"] = str(user["_id"])

     # remove sensitive fields
    user.pop("password", None)
    user.pop("createdAt", None)
    user.pop("updatedAt", None)
    user.pop("__v", None)


    return {
        "access_token": access_token,
        "user": user
    }
    


def register_user(data):

    users = get_users_collection()


    # Check email
    email_exists = users.find_one({
        "email": data["email"]
    })

    if email_exists:
        raise Exception("Email already exists")


    # Check phone
    phone_exists = users.find_one({
        "phone": data["phone"]
    })

    if phone_exists:
        raise Exception("Phone already exists")


    hashed_password = hash_password(
        data["password"]
    )


    user = user_schema(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        password=hashed_password
    )


    result = users.insert_one(user)


    user["_id"] = str(result.inserted_id)


    return user

def login_user(data):
    users = get_users_collection()

    user = users.find_one({
        "email": data["email"].lower()
    })

    if not user:
        raise Exception("Invalid email or password")

    if not check_password(
        data["password"],
        user["password"]
    ):
        raise Exception("Invalid email or password")

    access_token = generate_access_token({
        "userId": str(user["_id"]),
        "role": user["role"]
    })

    refresh_token = generate_refresh_token({
        "userId": str(user["_id"]),
        "role": user["role"]
    })

    user["_id"] = str(user["_id"])
  
    user.pop("password", None)
    user.pop("createdAt", None)
    user.pop("updatedAt", None)
    user.pop("__v", None)

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }