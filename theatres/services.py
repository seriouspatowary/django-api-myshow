from math import ceil
from common.mongodb import get_theatre_collection, get_screen_collection, get_seat_collection
from .models import seat_layout_schema, theatreSchema, screenSchema
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


def get_theatre(page, limit, userId,search=""):
    
    theatres = get_theatre_collection()
    screens = get_screen_collection()
    
    page = int(page)
    limit = int(limit)
    skip = (page-1)*limit
    
    query = {
       "userId": ObjectId(userId)
    }
    
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
        theatre["userId"] = str(theatre["userId"])
        
        
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
    theatre["userId"]= str(theatre["userId"])


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



    return screen


def get_theatre_list(userId):
    
    theatres = get_theatre_collection()
    
    result = theatres.find(
        {
            "userId":ObjectId(userId)
        },
        {
           "name":1
        }).sort("createdAt", -1)
    

    
    theatre_list = []
    
    for theatre in result:
         theatre["_id"] = str(theatre["_id"])
         theatre_list.append(theatre)
         
    return theatre_list



def get_theatre_screen_list(id):
    
    theatres = get_theatre_collection()
    screens = get_screen_collection()
    
    # validate theate exist
    
    theatre = theatres.find_one({"_id":ObjectId(id)})
    
    if not theatre:
        raise Exception("Theatre Not exist")
    
    result = screens.find(
        {
            "theatreId":ObjectId(id)
        },
         {
           "name":1
        }).sort("createdAt", -1)
    
    screen_list = []
    
    for screen in result:
         screen["_id"] = str(screen["_id"])
         screen_list.append(screen)
         
    return screen_list
    
    
def create_seat_layout(data,userId):
    
    seats = get_seat_collection()
    screens = get_screen_collection()
    
    # validate screen exist
    screen = screens.find_one({"_id":ObjectId(data["screenId"])})
    
    
    existing = seats.find_one({
     "screenId": ObjectId(data["screenId"])
      })

    if existing:
            raise Exception("Seat layout already exists for this screen")
    
    if not screen:
        raise Exception("Screen Not exist")
    
    seat = seat_layout_schema(
          userId= userId,
          screenId = data["screenId"],
          layout=data["layout"] 
        
     )
    
    result = seats.insert_one(seat)
    seat["_id"] = str(result.inserted_id)
    seat["screenId"] = str(seat["screenId"])
    seat["userId"] = str(seat["userId"])


    return seat


def get_seat_list(id):

    screens = get_screen_collection()
    seats = get_seat_collection()

    screen_id = ObjectId(id)

    # check theatre exists
    screen = screens.find_one({
        "_id": screen_id
    })

    if not screen:
        raise Exception("Screen Not Found")

 # Find seat layout
    result = seats.find_one(
        {"screenId": screen_id},
        {"layout": 1}
    )

    if not result:
        raise Exception("Seat layout not found for this screen")

    result["_id"] = str(result["_id"])

    return result


def get_seat_type(screenId):
    seats = get_seat_collection()

    seat_layout = seats.find_one(
        {"screenId": ObjectId(screenId)},
        {"layout": 1}
    )

    if not seat_layout:
        raise Exception("Seat layout not found")

    layout = seat_layout.get("layout", {})

    seat_types = set()
    total_seats = 0

    for row in layout.values():
        seat_types.add(row["seatType"])
        total_seats += row["seatCount"]

    return {
        "seatTypes": sorted(list(seat_types)),
        "totalSeats": total_seats
    }


    
    
    
    
    
 
