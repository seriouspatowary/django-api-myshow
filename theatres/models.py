from datetime import datetime
from bson import ObjectId



def theatreSchema(userId, name, address, city, contactNumber):
    now = datetime.utcnow()

    return {
        "userId": ObjectId(userId),
        "name": name.strip(),
        "address": address.strip(),
        "city": city.strip(),
        "contactNumber": contactNumber.strip(),
        "createdAt": now,
        "updatedAt": now
    }
      
def screenSchema(name,theatreId,totalSeats):
    
    now = datetime.utcnow()
    
    return{
        "name":name.strip(),
        "theatreId": ObjectId(theatreId),
        "totalSeats": totalSeats,
        "createdAt":now,
        "updatedAt":now
         
        
    }
    



def seat_layout_schema(userId, screenId, layout):
    now = datetime.utcnow()

    return {
        "userId": ObjectId(userId),
        "screenId": ObjectId(screenId),
        "layout": layout,
        "createdAt": now,
        "updatedAt": now
    }
    


# {
#   "screenId": "687d...",
#   "layout": {
#     "A": {
#       "seatCount": 10,
#       "seatType": "DIAMOND"
#     },
#     "B": {
#       "seatCount": 16,
#       "seatType": "GOLD"
#     },
#     "C": {
#       "seatCount": 16,
#       "seatType": "GOLD"
#     },
#     "D": {
#       "seatCount": 16,
#       "seatType": "GOLD"
#     }
#   }
# }