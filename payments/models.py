from datetime import datetime
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
):
    now = datetime.utcnow()

    return {
        "showId": ObjectId(show_id),
        "date": date,
        "time": time,
        "seats": seats,                  # ["A-3", "A-4"]
        "email": email.strip(),
        "mobile": mobile.strip(),
        "amount": amount,
        "razorpayOrderId": razorpay_order_id,
        "razorpayPaymentId": None,
        "status": "PENDING",             # PENDING -> PAID -> CANCELLED/EXPIRED
        "createdAt": now,
        "updatedAt": now,
    }