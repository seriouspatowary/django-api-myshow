from datetime import datetime
from bson import ObjectId




def theatreSchema(name, address, city,contactNumber):
      now = datetime.utcnow()
      
      return{
           "name": name.strip(),
           "address":address.strip(),
           "city": city.strip(),
           "contactNumber":contactNumber.strip(),
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
    
      