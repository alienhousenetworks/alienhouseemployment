from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from apps.accounts.views import login_view, logout_view, set_password_view, dashboard_view

urlpatterns = [
   

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('set-password/<uuid:uid>/<str:token>/', set_password_view),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view()),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view()),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view()),
    path('dashboard/', dashboard_view, name='dashboard'),
]
