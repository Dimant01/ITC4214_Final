from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Book
from .forms import BookForm
from django.db.models import Q
from accounts.models import UserActivity
from django.http import JsonResponse

def is_manager(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_manager)
def manager_catalog(request):

    query = request.GET.get("q")

    books = Book.objects.all().order_by('title')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    context = {
        "books": books,
        "query": query
    }

    return render(request, "catalog/manager_catalog.html", context)

@user_passes_test(is_manager)
def add_book(request):

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("manager_catalog")

    else:
        form = BookForm()

    return render(request, "catalog/book_form.html", {"form": form})

@user_passes_test(is_manager)
def edit_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":

        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            form.save()
            return redirect("manager_catalog")

    else:
        form = BookForm(instance=book)

    return render(request, "catalog/book_form.html", {"form": form})

@user_passes_test(is_manager)
def delete_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    book.delete()

    return redirect("manager_catalog")

def book_detail(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    # SIMILAR BOOKS LOGIC
    similar_books = Book.objects.filter(
        category=book.category
    ).exclude(id=book.id)

    # If the book has tags, use them for recommendations
    if book.tags.exists():
        similar_books = Book.objects.filter(
            tags__in=book.tags.all()
        ).exclude(id=book.id).distinct()

    similar_books = similar_books[:8]

    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            book=book,
            activity_type="view"
    )

    return render(request, "catalog/book_detail.html", {
        "book": book,
        "similar_books": similar_books
    })

@login_required
def toggle_like(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.user in book.liked_by.all():
        book.liked_by.remove(request.user)
        liked = False
    else:
        book.liked_by.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": book.liked_by.count()
    })