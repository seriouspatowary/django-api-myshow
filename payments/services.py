import razorpay
from datetime import datetime, timedelta
from django.conf import settings
from bson import ObjectId
from common.mongodb import get_shows_collection, get_booking_collection, get_users_collection
from .models import booking_schema


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)


def create_order(data):

    show_id = data["showId"]
    date = data["date"]
    time = data["time"]
    seats = data["seats"]
    email = data["email"]
    mobile = data["mobile"]

    shows = get_shows_collection()
    bookings = get_booking_collection()

    show = shows.find_one({
        "_id": ObjectId(show_id)
    })

    if not show:
        raise Exception("Show not found")

    if not seats:
        raise Exception("No seats selected")

    # Clear out abandoned pending locks so seats free up again
    cutoff = datetime.utcnow() - timedelta(minutes=10)
    bookings.delete_many({
        "status": "pending",
        "createdAt": {"$lt": cutoff},
    })

    conflict = bookings.find_one({
        "showId": ObjectId(show_id),
        "date": date,
        "time": time,
        "status": {"$in": ["pending", "paid"]},
        "seats": {"$in": seats},
    })

    if conflict:
        raise Exception("One or more seats are no longer available")

    layout = show["layout"]      # row letter -> {seatCount, seatType}
    prices = show["prices"]      # seatType -> price

    amount = 0
    for seat_id in seats:
        row = seat_id.split("-")[0]
        row_layout = layout.get(row)
        if not row_layout:
            raise Exception(f"Invalid seat: {seat_id}")
        seat_type = row_layout["seatType"]
        amount += prices[seat_type]

    order = client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1,
    })

    booking = booking_schema(
        show_id=show_id,
        date=date,
        time=time,
        seats=seats,
        email=email,
        mobile=mobile,
        amount=amount,
        razorpay_order_id=order["id"],
    )

    result = bookings.insert_one(booking)

    return {
        "bookingId": str(result.inserted_id),
        "orderId": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": settings.RAZORPAY_KEY_ID,
    }
    
    
def verify_payment(data):

    razorpay_order_id = data["razorpay_order_id"]
    razorpay_payment_id = data["razorpay_payment_id"]
    razorpay_signature = data["razorpay_signature"]

    # Verify signature
    client.utility.verify_payment_signature({
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    })

    bookings = get_booking_collection()

    booking = bookings.find_one({
        "razorpayOrderId": razorpay_order_id
    })

    if not booking:
        raise Exception("Booking not found")

    bookings.update_one(
        {
            "_id": booking["_id"]
        },
        {
            "$set": {
                "razorpayPaymentId": razorpay_payment_id,
                "paymentStatus": "SUCCESS",
                "status": "CONFIRMED",
                "updatedAt": datetime.utcnow()
            }
        }
    )

    return {
        "bookingId": str(booking["_id"]),
        "paymentId": razorpay_payment_id,
        "status": "CONFIRMED"
    }
    
    

def get_myorders(userId):
    users = get_users_collection()
    bookings = get_booking_collection()

    user = users.find_one({
        "_id": ObjectId(userId)
    })

    if not user:
        return []

    email = user["email"]

    pipeline = [
        {
            "$match": {
                "email": email,
                "status": "CONFIRMED",
                "paymentStatus": "SUCCESS"
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "email",
                "foreignField": "email",
                "as": "user"
            }
        },
        {
            "$unwind": "$user"
        },
        {
            "$lookup": {
                "from": "shows",
                "localField": "showId",
                "foreignField": "_id",
                "as": "show"
            }
        },
        {
            "$unwind": "$show"
        },
        {
            "$lookup": {
                "from": "movies",
                "localField": "show.movieId",
                "foreignField": "_id",
                "as": "movie"
            }
        },
        {
            "$unwind": "$movie"
        },
        {
            "$lookup": {
                "from": "screens",
                "localField": "show.screenId",
                "foreignField": "_id",
                "as": "screen"
            }
        },
        {
            "$unwind": "$screen"
        },
         {
            "$lookup": {
                "from": "theatres",
                "localField": "show.theatreId",
                "foreignField": "_id",
                "as": "theatre"
            }
        },
        {
            "$unwind": "$theatre"
        },
        {
            "$project": {
                "_id": 1,
                "showId": 1,
                "movieName": "$movie.title",
                 "theatreName": "$theatre.name",
                "screenName": "$screen.name",
                "language": "$show.language",
                "dimension": "$show.dimension",
                 
                "userName": "$user.name",
                "email": 1,
                "mobile": 1,
                "date": 1,
                "time": 1,
                "seats": 1,
                "amount": 1,
                "status": 1,
                "paymentStatus": 1,
                "createdAt": 1
            }
        },
        {
            "$sort": {
                "createdAt": -1
            }
        }
    ]

    orders = list(bookings.aggregate(pipeline))

    for order in orders:
        order["_id"] = str(order["_id"])
        order["showId"] = str(order["showId"])

    return orders