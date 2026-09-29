from django.urls import path
from django.contrib.auth import views as auth_views

from .views import home, create_profile, login_view


urlpatterns = [

    path("", home, name="home"),

    path("profile/", create_profile, name="create_profile"),

    path("login/", login_view, name="login"),

    # Forgot password
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="predictor/password_reset.html"
        ),
        name="password_reset"
    ),

    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="predictor/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="predictor/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="predictor/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]