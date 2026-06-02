from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from gestion.auth_views import register_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", register_view, name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/logout/", logout_view, name="logout"),
    path("api/", include("gestion.urls")),
]
