from django.urls import path
from . import views

urlpatterns = [
    path("manage/", views.manager_catalog, name="manager_catalog"),
    path("add/", views.add_book, name="add_book"),
    path("edit/<int:book_id>/", views.edit_book, name="edit_book"),
    path("delete/<int:book_id>/", views.delete_book, name="delete_book"),
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
]
