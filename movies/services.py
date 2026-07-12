from common.mongodb import get_movies_collection



def get_movies():

    movies = get_movies_collection()
    result = movies.find().sort("createdAt",-1)

    movie_list = []

    for movie in result:
        movie["_id"] = str(movie["_id"])
        movie_list.append(movie)


    return movie_list