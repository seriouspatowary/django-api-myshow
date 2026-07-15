from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from .views import MovieListAPIView, CreatedAPIView, deleteMovieAPIView, UpdateMovieAPIView


urlpatterns = [
    
    path("",MovieListAPIView.as_view()),
    path("add",CreatedAPIView.as_view()),
    path("update/<str:id>",UpdateMovieAPIView.as_view()),
    path("delete/<str:id>",deleteMovieAPIView.as_view())
    
]