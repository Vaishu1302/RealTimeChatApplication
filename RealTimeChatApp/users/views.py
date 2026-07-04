# from notifications.models import Notification
# from .models import GroupFile
from django.contrib.auth import logout
from django.utils import timezone
from django.shortcuts import render

from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
# from chat.models import GroupFile
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from notification.models import Notification
import random

from django.core.mail import send_mail
from django.contrib.auth.models import User

from .forms import (
    ForgotPasswordForm,
    OTPForm,
    ResetPasswordForm
)


def reset_password(request):

    if request.method == "POST":

        form = ResetPasswordForm(
            request.POST
        )

        if form.is_valid():

            p1 = form.cleaned_data[
                'password1'
            ]

            p2 = form.cleaned_data[
                'password2'
            ]

            if p1 == p2:

                user_id = request.session.get(
                    'reset_user'
                )

                user = User.objects.get(
                    id=user_id
                )

                user.set_password(
                    p1
                )

                user.save()

                request.session.flush()

                return redirect(
                    'login'
                )

            else:

                form.add_error(
                    'password2',
                    'Passwords do not match'
                )

    else:

        form = ResetPasswordForm()

    return render(
        request,
        'users/reset_password.html',
        {
            'form': form
        }
    )


def forgot_password(request):

    if request.method == "POST":

        form = ForgotPasswordForm(
            request.POST
        )

        if form.is_valid():

            email = form.cleaned_data['email']

            try:

                user = User.objects.get(
                    email=email
                )

                otp = random.randint(
                    100000,
                    999999
                )

                request.session['reset_otp'] = str(otp)

                request.session['reset_user'] = user.id

                send_mail(
                    'Password Reset OTP',
                    f'Your OTP is {otp}',
                    'yourgmail@gmail.com',
                    [email],
                    fail_silently=False
                )

                return redirect(
                    'verify_otp'
                )

            except User.DoesNotExist:

                form.add_error(
                    'email',
                    'Email not found'
                )

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        'users/forgot_password.html',
        {
            'form': form
        }
    )


def verify_otp(request):

    if request.method == "POST":

        form = OTPForm(
            request.POST
        )

        if form.is_valid():

            entered_otp = form.cleaned_data['otp']

            stored_otp = request.session.get(
                'reset_otp'
            )

            if entered_otp == stored_otp:

                return redirect(
                    'reset_password'
                )

            else:

                form.add_error(
                    'otp',
                    'Invalid OTP'
                )

    else:

        form = OTPForm()

    return render(
        request,
        'users/verify_otp.html',
        {
            'form': form
        }
    )


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = RegisterForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )

# @login_required


def user_login(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            user.profile.status = True
            user.profile.save()

            return redirect('dashboard')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'users/login.html',
        {'form': form}
    )

# @login_required


def user_logout(request):

    if request.user.is_authenticated:

        request.user.profile.status = False

        request.user.profile.last_seen = timezone.now()

        request.user.profile.save()

    logout(request)

    return redirect('login')


def dashboard(request):

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        'dashboard.html',
        {
            'unread_count': unread_count
        }
    )


# @login_required
# def profile(request):

#     if request.method == 'POST':

#         form = ProfileUpdateForm(
#             request.POST,
#             request.FILES,
#             instance=request.user.profile
#         )
#         if form.is_valid():
    #     profile = form.save(commit=False)

    #     if 'profile_picture-clear' in request.POST:
    #         profile.profile_picture = None

    #     profile.save()

    # if form.is_valid():
    #     if request.POST.get('profile_picture-clear'):
    #         request.user.profile.profile_picture.delete(save=False)
    #         request.user.profile.profile_picture = None
    #         request.user.profile.save()

    #     else:
    # form.save()

    # return redirect('profile')

    # else:

    #     form = ProfileUpdateForm(
    #         instance=request.user.profile
    #     )

    # return render(
    #     request,
    #     'users/profile.html',
    #     {'form': form}
    # )
@login_required
def profile(request):

    if request.method == 'POST':

        if request.POST.get('remove_picture'):

            request.user.profile.profile_picture.delete(save=False)

            request.user.profile.profile_picture = None

            request.user.profile.save()

            return redirect('profile')

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileUpdateForm(
            instance=request.user.profile
        )

    return render(
        request,
        'users/profile.html',
        {
            'form': form
        }
    )
