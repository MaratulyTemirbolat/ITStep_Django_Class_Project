from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)

from auths.models import CustomUser
from my_new_app.models import (
    StudentHomework,
)


class CustomUserRegisterForm(UserCreationForm):  # noqa
    email = forms.EmailField(label='Email/username',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control'}
                             ))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}
                                ))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}
                                ))

    class Meta:  # noqa
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class CustomerUserLoginForm(AuthenticationForm):  # noqa
    username = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class CreateHWForm(forms.ModelForm):  # noqa

    class Meta:  # noqa
        model = StudentHomework
        fields: tuple = (
            'title', 'subject',
            'logo'
        )
