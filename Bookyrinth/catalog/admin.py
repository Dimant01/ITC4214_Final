from django.contrib import admin
from .models import Book, Category, Tag

# Register your models here.

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Tag)
