from math import ceil
from common.mongodb import get_theatre_collection, get_screen_collection
from .models import theatreSchema, screenSchema
from bson import ObjectId


def create_theatre(data):
    
    theatres = get_theatre_collection()
    
    theatre = theatreSchema(
        name=data["name"],
        address=data["address"],
        city=data["city"],
        contactNumber=data["contactNumber"]
        
    )
    
    result = theatres.insert_one(theatre)
    
    theatre["_id"] = str(result.inserted_id)
    
    return theatre


def get_theatre(page, limit,search=""):
    
    theatres = get_theatre_collection()
    
    page = int(page)
    limit = int(limit)
    skip = (page-1)*limit
    
    query = {}
    
    if search:
        query ={
            "$or":[
                {"name":{"$regex":search,"$options":"i"}},
                {"city":{"$regex":search,"$options":"i"}},
                {"address":{"$regex":search,"$options":"i"}},
            ]
        }
    
    total = theatres.count_documents({})
    result = (
             theatres.find(query)
            .sort("createdAt",-1)
            .skip(skip)
            .limit(limit)
       )
    
    
    theatre_list = []
    
    for theatre in result:
        theatre["_id"] = str(theatre["_id"])
        theatre_list.append(theatre)
        
    return{
         "theatres":theatre_list,
         "pagination":{
             "page":page,
             "limit":limit,
             "total":total,
              "totalPages": ceil(total / limit)
              }
        
    }
    
def update_theatre(id,data):
    
        theatres = get_theatre_collection()
    
        theatre = theatreSchema(
            name=data["name"],
            address=data["address"],
            city=data["city"],
            contactNumber=data["contactNumber"]
            
        )
        
        result = theatres.update_one(
            {
                "_id":ObjectId(id)
            },
            {
                "$set":{
                    "name":data["name"],
                    "address":data["address"],
                    "city":data["city"],
                    "contactNumber":data["contactNumber"]
                }
            }
            
            )
        
        
        if result.matched_count == 0:
            raise Exception("Theatre Not Found")
        
        theatre = theatres.find_one({"_id":ObjectId(id)})
        
        theatre["_id"] = str(theatre["_id"])
        
        return theatre
    
def delete_theatre(id):
    theatre  = get_theatre_collection()
    
    result = theatre.delete_one({
        "_id": ObjectId(id)
    })
    
    if result.deleted_count == 0:
        raise Exception("Movie Not Found")
    
    return True


def create_screen(data):
    theatres = get_theatre_collection()
    screens = get_screen_collection()
    
    # validate theate exist
    
    theatre = theatres.find_one({"_id":ObjectId(data["theatreId"])})
    
    if not theatre:
        raise Exception("Theatre Not exist")
    
    screen = screenSchema(
          name= data["name"],
          theatreId = data["theatreId"],
          totalSeats=data["totalSeats"] 
        
     )
    
    result = screens.insert_one(screen)
    screen["_id"] = str(result.inserted_id)
    
    return screen
    
    
    
    
    
    
    
    
    
    
    
    
    
 
