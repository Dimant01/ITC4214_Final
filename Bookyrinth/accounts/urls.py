from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("users/", views.user_management, name="user_management"),
    path("users/promote/<int:user_id>/", views.promote_user, name="promote_user"),
    path("users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]