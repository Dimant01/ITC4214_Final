from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)

    author = models.CharField(max_length=100)

    isbn = models.CharField(max_length=13, unique=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    liked_by = models.ManyToManyField(
        User,
        blank=True,
        related_name="liked_books"
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="books/",
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title