from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def register_view(request):
    """
    User registration view with automatic sign-in upon successful creation.
    """
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to AURA, {user.first_name}! Your profile has been created.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors indicated below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    User authentication view with session persistence.
    """
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}.")
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('accounts:profile')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Terminates user session and redirects to storefront home.
    """
    auth_logout(request)
    messages.info(request, "You have been safely signed out.")
    return redirect('store:home')


@login_required
def profile_view(request):
    """
    Protected account profile view allowing users to view and update their personal details.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account details were successfully updated.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)
