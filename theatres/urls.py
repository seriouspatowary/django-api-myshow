
from django.urls import path
from .views import AddTheatreAPIView, GetThetreAPIView,UpdateAPIView,DeleteAPIView,AddScreenAPIView

urlpatterns = [
    path("add", AddTheatreAPIView.as_view()),
    path("", GetThetreAPIView.as_view()),
    path("update/<str:id>", UpdateAPIView.as_view()),
    path("delete/<str:id>", DeleteAPIView.as_view()),
    path("add-screen",AddScreenAPIView.as_view()),
    

]