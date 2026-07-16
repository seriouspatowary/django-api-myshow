from common.mongodb import get_movies_collection, get_casts_collection, get_crew_collection
from .models import movie_schema,cast_schema,crew_schema
from bson import ObjectId
from datetime import datetime
from math import ceil


def get_display_movies():
    movies = get_movies_collection()

    result = (
        movies.find(
            {},
            {
                "title": 1,
                "image":1
            }
        )
        .sort("createdAt", -1)
    )

    movie_list = []

    for movie in result:
        movie["_id"]=str(movie["_id"])
        movie_list.append(movie)
    return movie_list




def get_public_movies():
    movies = get_movies_collection()

    result = (
        movies.find(
            {},
            {
                "title": 1,
                "genre": 1,
                "image": 1,
            }
        )
        .sort("createdAt", -1)
    )

    movie_list = []

    for movie in result:
        movie["_id"] = str(movie["_id"])
        movie_list.append(movie)

    return movie_list




def get_movies(page=1, limit=10):
    movies = get_movies_collection()

    page = int(page)
    limit = int(limit)
    skip = (page - 1) * limit

    total = movies.count_documents({})

    result = (
        movies.find()
        .sort("createdAt", -1)
        .skip(skip)
        .limit(limit)
    )

    movie_list = []

    for movie in result:
        movie["_id"] = str(movie["_id"])
        movie_list.append(movie)

    return {
        "movies": movie_list,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": ceil(total / limit)
        }
    }


def create_movie(data):
    movies = get_movies_collection()
    movie = movie_schema(
        title=data["title"],
        genre=data["genre"],
        image=data["image"],
        description=data["description"],
        duration=data["duration"],
        language=data["language"],
        dimension=data["dimension"],
        release_date=datetime.fromisoformat(data["releaseDate"])
        if isinstance(data["releaseDate"], str)
        else data["releaseDate"],
    )

    result = movies.insert_one(movie)
    movie["_id"] = str(result.inserted_id)

    return movie



def update_movie(movie_id,data):

    movies = get_movies_collection()

    result = movies.update_one(
        {
            "_id":ObjectId(movie_id)
        },

        {
            "$set": {
                "title": data["title"],
                "genre": data["genre"],
                "image": data["image"],
                "description": data["description"],
                "duration": data["duration"],
                "language": data["language"],
                "dimension": data["dimension"],
                "releaseDate": data["releaseDate"],
                "updatedAt": datetime.utcnow()
             }
        }
        
        )
    if result.matched_count == 0:
        raise Exception("Movie not found")
    
    movie = movies.find_one(
              {
                  "_id": ObjectId(movie_id)
              }
              )
    
    movie["_id"] = str(movie["_id"])

    return movie



def delete_movie(movie_id):

    movies = get_movies_collection()

    result = movies.delete_one(
        {
            "_id":ObjectId(movie_id)
        }
    )

    if result.deleted_count == 0:
        raise Exception("Movie Not found")
    
    return True


def create_movie_cast(data):
    movies = get_movies_collection()
    casts =  get_casts_collection()

    # validate movie exists

    movie = movies.find_one({"_id":ObjectId(data["movieId"])})

    if not movie:
        raise Exception("Movie Not Found")
    
    cast = cast_schema(
            movieId=data["movieId"],
            name= data["name"],
            character=data["character"],
            image= data["image"],
       )
    result = casts.insert_one(cast)

    cast["_id"] = str(result.inserted_id)
    cast["movieId"] = str(cast["movieId"])

    return cast


def create_movie_crew(data):
    
        movies = get_movies_collection()
        crews =  get_crew_collection()

        # validate movie exists
        movie = movies.find_one({"_id":ObjectId(data["movieId"])})

        if not movie:
            raise Exception("Movie Not Found")
        
        crew = crew_schema(
                movieId=data["movieId"],
                name= data["name"],
                role=data["role"],
                image= data["image"],
        )
        result = crews.insert_one(crew)

        crew["_id"] = str(result.inserted_id)
        crew["movieId"] = str(crew["movieId"])

        return crew

        




def get_movie_cast_by_movieId(movieId):
    casts = get_casts_collection()

    result = casts.find({"movieId": ObjectId(movieId)})

    cast_list = []

    for cast in result:
        cast["_id"] = str(cast["_id"])
        cast["movieId"] = str(cast["movieId"])
        cast_list.append(cast)

    return cast_list


def get_movie_crew_by_movieId(movieId):
    crews = get_crew_collection()

    crew = crews.find({"movieId": ObjectId(movieId)})

    crew_list = []
    
    for crew in crews:
        crew["_id"] = str(crew["_id"])
        crew["movieId"] = str(crew["movieId"])
        crew_list.append(crew)

    return crew_list
