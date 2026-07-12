from datetime import datetime


class UserRole:
    USER = "user"
    ADMINISTRATOR = "administrator"


def user_schema(
    name,
    email,
    phone,
    password,
    role=UserRole.USER
):
    now = datetime.utcnow()

    return {
        "name": name,
        "email": email.lower().strip(),
        "phone": phone.strip(),
        "password": password,
        "role": role,
        "createdAt": now,
        "updatedAt": now
    }