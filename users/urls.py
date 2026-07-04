from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register,
    user_login,
    user_logout,
    dashboard,
    profile,
    forgot_password,
    reset_password,
    verify_otp,
    
)

urlpatterns = [

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        user_login,
        name='login'
    ),

    path(
        'logout/',
        user_logout,
        name='logout'
    ),

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),
    path(
        'profile/',
        profile,
        name='profile'
    ),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
        'forgot-password/',
        forgot_password,
        name='forgot_password'
    ),

    path(
        'forgot-password/',
        forgot_password,
        name='forgot_password'
    ),

    path(
        'verify-otp/',
        verify_otp,
        name='verify_otp'
    ),

    path(
        'reset-password/',
        reset_password,
        name='reset_password'
    )


]
