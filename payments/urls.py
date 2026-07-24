from django.urls import path
from .views import CreateOrderAPIView,VerifyPaymentAPIView,MyOrderAPIView


urlpatterns=[
    path("create-order/",CreateOrderAPIView.as_view()),
    path("verify/",VerifyPaymentAPIView.as_view()),
    path("myorder/",MyOrderAPIView.as_view())
    
]