import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30




def verify_refresh_token(token):

    return jwt.decode(
        token,
        settings.REFRESH_SECRET,
        algorithms=["HS256"]
    )


def generate_access_token(payload):
    data = payload.copy()

    data["exp"] = (
        datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return jwt.encode(
        data,
        settings.ACCESS_SECRET,
        algorithm="HS256"
    )


def generate_refresh_token(payload):
    data = payload.copy()

    data["exp"] = (
        datetime.now(timezone.utc)
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return jwt.encode(
        data,
        settings.REFRESH_SECRET,
        algorithm="HS256"
    )