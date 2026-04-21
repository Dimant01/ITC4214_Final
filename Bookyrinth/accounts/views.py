from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from datetime import date

from .models import Profile, UserActivity
from .forms import ProfileForm, UserUpdateForm

from catalog.models import Book, Tag


# =========================
# AUTH
# =========================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('home')


# =========================
# ADMIN MANAGEMENT
# =========================

def is_manager(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_manager)
def user_management(request):
    users = User.objects.all().order_by("-date_joined")

    return render(request, "accounts/user_management.html", {
        "users": users
    })


@user_passes_test(is_manager)
def promote_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_staff = True
    user.save()
    return redirect("user_management")

@user_passes_test(is_manager)
def demote_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_staff = False
    user.save()
    return redirect("user_management")


@user_passes_test(is_manager)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.warning(request, "To delete your account, please go to the profile page.")
        return redirect("user_management")

    if not user.is_superuser:
        user.delete()

    return redirect("user_management")
# =========================
# PROFILE VIEW
# =========================

@login_required
def profile_view(request):

    profile, _ = Profile.objects.get_or_create(user=request.user)

    today = date.today()

    is_birthday = False

    if profile.birth_date:
        is_birthday = (
            profile.birth_date.month == today.month and
            profile.birth_date.day == today.day
        )

    recent_views = UserActivity.objects.filter(
        user=request.user,
        activity_type="view"
    )[:10]

    cart_actions = UserActivity.objects.filter(
        user=request.user,
        activity_type="cart_add"
    )[:10]

    purchases = UserActivity.objects.filter(
        user=request.user,
        activity_type="purchase"
    )[:10]

    # =========================
    # LIKED BOOKS
    # =========================
    liked_books = request.user.liked_books.all()

    # =========================
    # RECOMMENDATIONS
    # based on:
    # - same category
    # - same author
    # - overlapping tags
    # =========================

    recommended_books = Book.objects.filter(
        Q(category__in=liked_books.values("category")) |
        Q(author__in=liked_books.values("author")) |
        Q(tags__in=Tag.objects.filter(book__in=liked_books))
    ).exclude(
        id__in=liked_books.values("id")
    ).distinct()[:10]

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "recent_views": recent_views,
        "cart_actions": cart_actions,
        "purchases": purchases,
        "liked_books": liked_books,
        "recommended_books": recommended_books,
        "is_birthday": is_birthday,
    })


# =========================
# EDIT PROFILE
# =========================

@login_required
def edit_profile(request):

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        profile_form = ProfileForm(request.POST, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():

            user_form.save()
            profile_form.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {
        "profile_form": profile_form,
        "user_form": user_form
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("home")