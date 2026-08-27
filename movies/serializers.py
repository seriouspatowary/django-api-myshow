class MovieSerializer:

    @staticmethod
    def serialize(movie):
        return {
            "_id": str(movie["_id"]),
            "title": movie["title"],
            "genre": movie["genre"],
            "image": movie["image"],
        }
        
        

class CastSerializer:
    
    @staticmethod
    
    def serialize(cast):
        return {
            "_id": str(cast["_id"]),
            "movieId": str(cast["movieId"]),
            "name": cast["name"],
            "character": cast["character"],
            "image": cast["image"],
        }
        
        
        
class CrewSerializer:
    @staticmethod
    
    def serialize(crew):
        return {
            "_id": str(crew["_id"]),
            "movieId": str(crew["movieId"]),
            "name": crew["name"],
            "designation": crew["designation"],
            "image": crew["image"],
        }