from common.mongodb import get_movies_collection
from .models import movie_schema
from bson import ObjectId


def create_movie(data):
    movies = get_movies_collection()

    movie = movie_schema(
        title=data["title"],
        genre=data["genre"],
        image=data["image"]
    )
    result = movies.insert_one(movie)
    movie["_id"] = str(result.inserted_id)

    return movie



def get_movies():

    movies = get_movies_collection()
    result = movies.find().sort("createdAt",-1)

    movie_list = []

    for movie in result:
        movie["_id"] = str(movie["_id"])
        movie_list.append(movie)


    return movie_list


def update_movie(movie_id,data):

    movies = get_movies_collection()

    result = movies.update_one(
        {
            "_id":ObjectId(movie_id)
        },

        {
            "$set":{
                "title":data["title"],
                "genre":data["genre"],
                "image": data["image"]
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
