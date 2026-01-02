from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from .models import User


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        user = form.get_user()
        login(request, user)

        # LONG LOGIN SUPPORT
        if user.role == 'ADMIN':
            request.session.set_expiry(60 * 60 * 24)      # 1 day
        else:
            request.session.set_expiry(60 * 60 * 24 * 90) # 90 days

        return redirect('dashboard')

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# SIGNUP DISABLED
def signup_view(request):
    return redirect('login')


def set_password_view(request, uid, token):
    user = get_object_or_404(User, pk=uid)

    if not default_token_generator.check_token(user, token):
        return render(request, 'auth/invalid_link.html')

    form = SetPasswordForm(user, request.POST or None)
    if form.is_valid():
        form.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'auth/set_password.html', {'form': form})
