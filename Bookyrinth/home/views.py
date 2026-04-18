from django.shortcuts import render
from catalog.models import Book, Category, Tag
from django.db.models import Q
from django.core.paginator import Paginator


def home(request):

    books = Book.objects.all()

    # =========================
    # SEARCH
    # =========================
    search_query = request.GET.get("search")
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )

    # =========================
    # CATEGORY FILTER
    # =========================
    selected_categories = request.GET.getlist("category")
    if selected_categories:
        books = books.filter(category__id__in=selected_categories)

    # =========================
    # TAG FILTER
    # =========================
    selected_tags = request.GET.getlist("tag")
    if selected_tags:
        books = books.filter(tags__id__in=selected_tags).distinct()

    # =========================
    # PAGINATION (JS-controlled)
    # =========================
    page_size = request.GET.get("page_size", 12)

    try:
        page_size = int(page_size)
    except ValueError:
        page_size = 12

    paginator = Paginator(books, page_size)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)

    # =========================
    # CONTEXT
    # =========================
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        "books": books,
        "categories": categories,
        "tags": tags,
        "selected_categories": selected_categories,
        "selected_tags": selected_tags,
        "search_query": search_query
    }

    return render(request, "home/home.html", context)