from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


# class RegisterForm(UserCreationForm):

#     email = forms.EmailField()

#     class Meta:
#         model = User

#         fields = [
#             'username',
#             'email',
#             'password1',
#             'password2'
#         ]
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    'class': 'form-control'
                }
            )


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = ['profile_picture']


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField()


class OTPForm(forms.Form):

    otp = forms.CharField(
        max_length=6
    )


class ResetPasswordForm(forms.Form):

    password1 = forms.CharField(
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput
    )
