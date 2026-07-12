from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "success": True,
        "message": "MyShow API Server Running"
    })


urlpatterns = [
    path("", home),

    path("admin/", admin.site.urls),

    path("api/auth/", include("accounts.urls")),
    path("api/movie/", include("movies.urls")),

]