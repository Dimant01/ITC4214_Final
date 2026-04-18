from django.contrib import admin
from .models import Book, Category, Tag

#Register your models here

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "price", "stock", "safe_image")

    def safe_image(self, obj):
        if obj.image:
            try:
                return obj.image.url
            except:
                return "Broken image"
        return "No image"

    safe_image.short_description = "Image"


admin.site.register(Category)
admin.site.register(Tag)