from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from .views import MovieListAPIView


urlpatterns = [
    
    path("",MovieListAPIView.as_view())
    
    
]