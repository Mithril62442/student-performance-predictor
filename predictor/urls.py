from django.urls import path
from .views import home, create_profile


urlpatterns = [
    path("", home, name="home"),
    path("profile/", create_profile, name="create_profile"),
]