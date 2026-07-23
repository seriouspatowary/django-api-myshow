from math import ceil
from common.mongodb import get_shows_collection,get_seat_collection
from .models import show_schema
from datetime import datetime
from bson import ObjectId


def create_show(data, userId):
    shows = get_shows_collection()
    seats = get_seat_collection()

    screenId = ObjectId(data["screenId"])

    # Get seat layout
    seat_layout = seats.find_one(
        {
            "screenId": screenId
        },
        {
            "layout": 1
        }
    )

    if not seat_layout:
        raise Exception("Seat layout not found for this screen")

    layout = seat_layout["layout"]

    show = show_schema(
        userId=userId,
        movieId=data["movieId"],
        theatreId=data["theatreId"],
        screenId=data["screenId"],
        availableSeats=data["availableSeats"],
        prices=data["prices"],
        schedule=data["schedule"],
        layout=layout,
        dimension=data["dimension"],
        language=data["language"]
    )

    result = shows.insert_one(show)

    show["_id"] = str(result.inserted_id)
    show["userId"] = str(show["userId"])
    show["theatreId"] = str(show["theatreId"])
    show["screenId"] = str(show["screenId"])
    show["movieId"] = str(show["movieId"])

    return show


def get_shows(userId, page=1, limit=10):
    shows = get_shows_collection()

    page = int(page)
    limit = int(limit)

    skip = (page - 1) * limit

    query = {
        "userId": ObjectId(userId)
    }

    total = shows.count_documents(query)

    result = (
        shows.find(query)
        .sort("createdAt", -1)
        .skip(skip)
        .limit(limit)
    )

    show_list = []

    for show in result:

        show["_id"] = str(show["_id"])
        show["userId"] = str(show["userId"])
        show["movieId"] = str(show["movieId"])
        show["theatreId"] = str(show["theatreId"])
        show["screenId"] = str(show["screenId"])

        show_list.append(show)

    return {
        "shows": show_list,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": ceil(total / limit)
        }
    }


def update_show(data, showId, userId):

    shows = get_shows_collection()

    show = shows.find_one({
        "_id": ObjectId(showId),
        "userId": ObjectId(userId)
    })

    if not show:
        raise Exception("Show not found")

    update_data = {}

    if "prices" in data:
        update_data["prices"] = data["prices"]

    if "schedule" in data:
        update_data["schedule"] = data["schedule"]

    if "dimension" in data:
        update_data["dimension"] = data["dimension"]

    if "language" in data:
        update_data["language"] = data["language"]

    # Don't allow these to be updated
    # availableSeats
    # layout
    # movieId
    # theatreId
    # screenId

    update_data["updatedAt"] = datetime.utcnow()

    result = shows.update_one(
        {
            "_id": ObjectId(showId),
            "userId": ObjectId(userId)
        },
        {
            "$set": update_data
        }
    )

    if result.modified_count == 0:
        raise Exception("No changes made")

    updated_show = shows.find_one({
        "_id": ObjectId(showId)
    })

    updated_show["_id"] = str(updated_show["_id"])
    updated_show["userId"] = str(updated_show["userId"])
    updated_show["movieId"] = str(updated_show["movieId"])
    updated_show["theatreId"] = str(updated_show["theatreId"])
    updated_show["screenId"] = str(updated_show["screenId"])

    return updated_show


def get_show_byId(showId):

    shows = get_shows_collection()

    pipeline = [

        {
            "$match": {
                "_id": ObjectId(showId)
            }
        },

        # Join movie
        {
            "$lookup": {
                "from": "movies",
                "localField": "movieId",
                "foreignField": "_id",
                "as": "movie"
            }
        },

        {
            "$unwind": "$movie"
        },


        # Join theatre
        {
            "$lookup": {
                "from": "theatres",
                "localField": "theatreId",
                "foreignField": "_id",
                "as": "theatre"
            }
        },

        {
            "$unwind": "$theatre"
        },


        # Join screen
        {
            "$lookup": {
                "from": "screens",
                "localField": "screenId",
                "foreignField": "_id",
                "as": "screen"
            }
        },

        {
            "$unwind": "$screen"
        },


        # Select required fields
        {
            "$project": {

                "_id": 1,

                "movieId": 1,
                "movieName": "$movie.title",

                "theatreId": 1,
                "theatreName": "$theatre.name",

                "screenId": 1,
                "screenName": "$screen.name",

                "availableSeats": 1,
                "prices": 1,
                "schedule": 1,

                "createdAt": 1,
                "updatedAt": 1
            }
        }
    ]


    result = list(shows.aggregate(pipeline))


    if not result:
        raise Exception("Show not found")


    show = result[0]


    # Convert ObjectIds
    show["_id"] = str(show["_id"])
    show["movieId"] = str(show["movieId"])
    show["theatreId"] = str(show["theatreId"])
    show["screenId"] = str(show["screenId"])


    return show



def get_shows_by_movie(movieId, language, dimension):
    shows = get_shows_collection()

    pipeline = [
        {
            "$match": {
                "movieId": ObjectId(movieId),
                "language": language,
                "dimension": dimension
            }
        },
        {
            "$lookup": {
                "from": "movies",
                "localField": "movieId",
                "foreignField": "_id",
                "as": "movie"
            }
        },
        {
            "$unwind": "$movie"
        },
        {
            "$lookup": {
                "from": "theatres",
                "localField": "theatreId",
                "foreignField": "_id",
                "as": "theatre"
            }
        },
        {
            "$unwind": "$theatre"
        },
        {
            "$lookup": {
                "from": "screens",
                "localField": "screenId",
                "foreignField": "_id",
                "as": "screen"
            }
        },
        {
            "$unwind": "$screen"
        },
        {
            "$project": {
                "_id": 1,
                "movieId": 1,
                "movieName": "$movie.title",
                "genre":"$movie.genre",
                "duration":"$movie.duration",

                "theatreId": 1,
                "theatreName": "$theatre.name",

                "screenId": 1,
                "screenName": "$screen.name",

                "language": 1,
                "dimension": 1,
                "prices": 1,
                "schedule": 1,
                "availableSeats": 1
            }
        },
        {
            "$sort": {
                "theatreName": 1
            }
        }
    ]

    result = list(shows.aggregate(pipeline))

    for show in result:
        show["_id"] = str(show["_id"])
        show["movieId"] = str(show["movieId"])
        show["theatreId"] = str(show["theatreId"])
        show["screenId"] = str(show["screenId"])

    return result



def get_layout_by_show(showId):
    shows = get_shows_collection()

    pipeline = [
        {
            "$match": {
                "_id": ObjectId(showId)
            }
        },
        {
            "$lookup": {
                "from": "movies",
                "localField": "movieId",
                "foreignField": "_id",
                "as": "movie"
            }
        },
        {
            "$unwind": "$movie"
        },
        {
            "$lookup": {
                "from": "theatres",
                "localField": "theatreId",
                "foreignField": "_id",
                "as": "theatre"
            }
        },
        {
            "$unwind": "$theatre"
        },
        {
            "$lookup": {
                "from": "screens",
                "localField": "screenId",
                "foreignField": "_id",
                "as": "screen"
            }
        },
        {
            "$unwind": "$screen"
        },
        {
            "$project": {
                "_id": 1,
                "movieId": 1,
                "movieName": "$movie.title",
                "genre": "$movie.genre",
                "duration": "$movie.duration",
                "image": "$movie.image",

                "theatreId": 1,
                "theatreName": "$theatre.name",
                "theatreAddress": "$theatre.address",

                "screenId": 1,
                "screenName": "$screen.name",

                "language": 1,
                "dimension": 1,
                "prices": 1,
                "schedule": 1,
                "layout": 1,
                "availableSeats": 1
            }
        }
    ]

    result = list(shows.aggregate(pipeline))

    if not result:
        return None

    show = result[0]

    show["_id"] = str(show["_id"])
    show["movieId"] = str(show["movieId"])
    show["theatreId"] = str(show["theatreId"])
    show["screenId"] = str(show["screenId"])

    return show

    
