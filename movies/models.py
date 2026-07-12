from datetime import datetime


def  movie_schema(title,genre,image):
      
      now = datetime.utcnow()


      return {
            
             "title":title.strip(),
             "genre": genre.strip(),
             "image": image.strip(),
             "createdAt": now,
             "updatedAt": now,
      }