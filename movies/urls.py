from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from .views import MovieListAPIView, CreatedAPIView, deleteMovieAPIView, UpdateMovieAPIView, PublicMovieListAPIView,castAddAPIView,displaynameAPIView, MovieCastDetailAPIView,crewAddAPIView, MovieCrewDetailAPIView


urlpatterns = [

   
    path("public",PublicMovieListAPIView.as_view()),
    path("admin",MovieListAPIView.as_view()),
    path("add",CreatedAPIView.as_view()),
    path("update/<str:id>",UpdateMovieAPIView.as_view()),
    path("delete/<str:id>",deleteMovieAPIView.as_view()),
    path("display",displaynameAPIView.as_view()),
     
    # casting
   
    path("cast/add",castAddAPIView.as_view()),
    path("cast/<str:movieId>", MovieCastDetailAPIView.as_view()),
    
    #crew
    
    path("crew/add",crewAddAPIView.as_view()),
    path("crew/<str:movieId>", MovieCrewDetailAPIView.as_view()),
    
]