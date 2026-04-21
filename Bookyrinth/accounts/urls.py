from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("users/", views.user_management, name="user_management"),
    path("users/promote/<int:user_id>/", views.promote_user, name="promote_user"),
    path("users/demote/<int:user_id>/", views.demote_user, name="demote_user"),
    path("users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path(
    "password_change/",
    auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html"
    ),
    name="password_change"
),

path(
    "password_change_done/",
    auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"
    ),
    name="password_change_done"
),
]