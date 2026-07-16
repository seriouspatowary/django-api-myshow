from datetime import datetime
from bson import ObjectId


def movie_schema(
    title,
    genre,
    image,
    description,
    duration,
    language,
    dimension,
    release_date,
):
    now = datetime.utcnow()

    return {
        "title": title.strip(),
        "genre": genre.strip(),
        "image": image.strip(),
        "description": description.strip(),
        "duration": duration,          # e.g. 169 (minutes)
        "language": language.strip(),  # e.g. English, Hindi
        "dimension": dimension.strip(),# e.g. 2D, 3D, IMAX 3D, 4DX
        "releaseDate": release_date,   # datetime object or ISO string
        "createdAt": now,
        "updatedAt": now,
    }


def cast_schema(movieId,name,character,image):
      now = datetime.utcnow()

      return{
            "movieId":ObjectId(movieId),
            "name": name.strip(),
            "character": character.strip(),
            "image": image.strip(),
            "createdAt": now,
            "updatedAt": now,
      }


def crew_schema(movieId, name, role, image):
    now = datetime.utcnow()

    return {
        "movieId": ObjectId(movieId),
        "name": name.strip(),
        "role": role.strip(),   # Director, Producer, Writer, Music Director, etc.
        "image": image.strip(),
        "createdAt": now,
        "updatedAt": now,
    }