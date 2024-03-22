from django.urls import path, include
# from .views import


urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/register/", include("dj_rest_auth.registration.urls")),
]
