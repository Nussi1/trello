from django.urls import path, include
from .views import dashboard, register

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("oauth/", include("social_django.urls")),
    path("register/", register, name="register"),
]