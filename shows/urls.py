from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from .views import ShowListAPIView, AddShowPIView,EditShowAPIView, GetShowByIdAPIView,GetShowByMovieAPIView, GetLayoutByShowAPIView

urlpatterns = [
    path("add", AddShowPIView.as_view()),
    path("list", ShowListAPIView.as_view()),
    path("update/<str:showId>",EditShowAPIView.as_view()),
    path("getshow/<str:showId>",GetShowByIdAPIView.as_view()),
    path("allshow/<str:movieId>",GetShowByMovieAPIView.as_view()),
    path("layout/<str:showId>",GetLayoutByShowAPIView.as_view())
    
    
]