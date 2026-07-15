from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from bson import ObjectId

from .jwt import verify_access_token
from .mongodb import get_users_collection


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid token")

        token = auth_header.split(" ")[1]

        try:
            payload = verify_access_token(token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")

        users = get_users_collection()

        user = users.find_one({
            "_id": ObjectId(payload["userId"])
        })

        if not user:
            raise AuthenticationFailed("User not found")

        user["_id"] = str(user["_id"])

        return (user, None)