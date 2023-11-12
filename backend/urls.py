from django.contrib import admin
from django.urls import path, include
from api.views import TimeslotViewSet
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', include('api.urls')),
]
