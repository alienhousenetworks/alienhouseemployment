

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm

from apps.accounts.models import User
from apps.accounts.forms import CustomAuthenticationForm
from apps.core.permissions import is_admin, is_manager, is_employee

def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        if user.is_superuser or is_admin(user):
            request.session.set_expiry(60 * 60 * 24)
            return redirect('admin:index')

        elif is_manager(user):
            request.session.set_expiry(60 * 60 * 24 * 30)
            return redirect('organization:manager_dashboard')

        elif is_employee(user):
            request.session.set_expiry(60 * 60 * 24 * 90)
            return redirect('dashboard')

        return redirect('login')

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

@login_required
def dashboard_view(request):
    if request.user.role == 'EMPLOYEE':
        return redirect('organization:employee_dashboard')
    elif request.user.role == 'MANAGER':
        return redirect('organization:manager_dashboard')
    else:
        # Admin or other - redirect to home page instead of admin
        return redirect('core:home_view')
