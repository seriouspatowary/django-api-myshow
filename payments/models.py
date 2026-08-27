from datetime import datetime, timedelta
from bson import ObjectId

def booking_schema(
    show_id,
    date,
    time,
    seats,
    email,
    mobile,
    amount,
    razorpay_order_id,
    expires_at,
):
    now = datetime.utcnow()

    return {
        "showId": ObjectId(show_id),
        "date": date,
        "time": time,

        "seats": seats,

        "email": email.strip(),
        "mobile": mobile.strip(),

        "amount": amount,

        "razorpayOrderId": razorpay_order_id,
        "razorpayPaymentId": None,

        "status": "pending",

        "lockExpiresAt": expires_at,

        "createdAt": now,
        "updatedAt": now,
    }
    
    
    
    
    
    
def seat_lock_schema(
    show_id,
    date,
    time,
    seat_id,
    booking_id,
    expires_at,
):
    return {
        "showId": ObjectId(show_id),
        "date": date,
        "time": time,
        "seatId": seat_id,
        "bookingId": ObjectId(booking_id),
        "expiresAt": expires_at,
        "createdAt": datetime.utcnow(),
    }