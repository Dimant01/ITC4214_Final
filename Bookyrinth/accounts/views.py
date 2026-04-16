from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm
from django.contrib import messages
from .models import UserActivity

# Create your views here.

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
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        return redirect("user_management")

    if not user.is_superuser:
        user.delete()

    return redirect("user_management")

@login_required
def profile_view(request):

    profile = Profile.objects.get(user=request.user)

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

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "recent_views": recent_views,
        "cart_actions": cart_actions,
        "purchases": purchases,
    })

@login_required
def edit_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {
        "form": form
    })
