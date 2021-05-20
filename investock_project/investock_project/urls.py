from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('investock_app.urls')),
    path('admin/', admin.site.urls),
    path("auth", include("rest_framework.urls")),
]
