
from django.urls import path
from .views import AddTheatreAPIView, GetThetreAPIView,UpdateAPIView,DeleteAPIView,AddScreenAPIView,TheatreListAPIView,screenListAPIView,SeatsAddAPIView,GetSeatLayoutAPIView,GetSeatTypeAPIView

urlpatterns = [
    path("add", AddTheatreAPIView.as_view()),
    path("", GetThetreAPIView.as_view()),
    path("update/<str:id>", UpdateAPIView.as_view()),
    path("delete/<str:id>", DeleteAPIView.as_view()),
    path("add-screen",AddScreenAPIView.as_view()),
    
    path("list",TheatreListAPIView.as_view()),
    path("screen/<str:id>", screenListAPIView.as_view()),
    
    path("add-seats", SeatsAddAPIView.as_view()),
    path("get-seats/<str:id>",GetSeatLayoutAPIView.as_view()),
    path("get-distinct-type/<str:id>", GetSeatTypeAPIView.as_view())

]