from bson import ObjectId
from datetime import datetime


def show_schema(
    userId,
    movieId,
    theatreId,
    screenId,
    availableSeats,
    prices,
    schedule,
    layout,
    dimension,
    language,
):
    now = datetime.utcnow()

    return {
        "userId": ObjectId(userId),
        "movieId": ObjectId(movieId),
        "theatreId": ObjectId(theatreId),
        "screenId": ObjectId(screenId),
        "availableSeats": availableSeats,
        "prices": prices,
        "layout": layout,
        "schedule": schedule,
        "dimension": dimension,
        "language":language,
        "createdAt": now,
        "updatedAt": now
    }