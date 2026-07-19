from math import ceil
from common.mongodb import get_theatre_collection, get_screen_collection
from .models import theatreSchema, screenSchema
from bson import ObjectId
from datetime import datetime


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
    screens = get_screen_collection()
    
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
        theatre_id = theatre["_id"]
        
        theatre["_id"] = str(theatre["_id"])
        
        
        # fetch screens
        screen_list = list(screens.find({"theatreId":ObjectId(theatre_id)}))
        
        for screen in screen_list:
            screen["_id"] = str(screen["_id"])
            screen["theatreId"] = str(screen["theatreId"])
        
        theatre["screens"] = screen_list 
        
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
    
    
    
    
    
def update_theatre(id, data):

    theatres = get_theatre_collection()
    screens = get_screen_collection()

    theatre_id = ObjectId(id)

    # update theatre
    result = theatres.update_one(
        {
            "_id": theatre_id
        },
        {
            "$set": {
                "name": data["name"],
                "address": data["address"],
                "city": data["city"],
                "contactNumber": data["contactNumber"],
                "updatedAt": datetime.utcnow()
            }
        }
    )


    if result.matched_count == 0:
        raise Exception("Theatre Not Found")


    # handle screens
    if "screens" in data and data["screens"]:

        for screen_data in data["screens"]:

            # existing screen update
            if "_id" in screen_data:

                screen_result = screens.update_one(
                    {
                        "_id": ObjectId(screen_data["_id"]),
                        "theatreId": theatre_id
                    },
                    {
                        "$set": {
                            "name": screen_data["name"],
                            "totalSeats": screen_data["totalSeats"],
                            "updatedAt": datetime.utcnow()
                        }
                    }
                )


            # new screen create
            else:

                screen = screenSchema(
                    name=screen_data["name"],
                    theatreId=id,
                    totalSeats=screen_data["totalSeats"]
                )

                screens.insert_one(screen)



    # fetch updated theatre
    theatre = theatres.find_one({
        "_id": theatre_id
    })


    theatre["_id"] = str(theatre["_id"])


    # fetch screens
    screen_list = list(
        screens.find({
            "theatreId": theatre_id
        })
    )


    for screen in screen_list:
        screen["_id"] = str(screen["_id"])
        screen["theatreId"] = str(screen["theatreId"])


    theatre["screens"] = screen_list


    return theatre
    

def delete_theatre(id):
    theatres  = get_theatre_collection()
    screens = get_screen_collection()

    theatre_id = ObjectId(id)

    # check theatre exists
    theatre = theatres.find_one({
        "_id": theatre_id
    })

    if not theatre:
        raise Exception("Theatre Not Found")


    # delete all screens of this theatre
    screens.delete_many({
        "theatreId": theatre_id
    })


    # delete theatre
    result = theatres.delete_one({
        "_id": theatre_id
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
    screen["theatreId"] = str(screen["theatreId"])
    
    print(screen)


    return screen
    
    
    
    
    
    
    
    
    
    
    
    
    
 
