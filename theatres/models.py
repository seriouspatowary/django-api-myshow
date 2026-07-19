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
        "theatreId": theatreId.strip(),
        "totalSeats": totalSeats.strip(),
        "createdAt":now,
        "updatedAt":now
         
        
    }
    
      