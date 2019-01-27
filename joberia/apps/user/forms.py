from django import forms

from joberia.apps.user.models import User


class RegisterForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email address'
        })
    )
    new_username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username',
        }),
        label='Username'
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'maxlength': '150', 'minlength': '4'
        }),
        label='Password'
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'repeat password',
            'maxlength': '150', 'minlength': '4'
        }),
        label='Repeat password'
    )

    role = forms.ChoiceField(
        widget=forms.RadioSelect, choices=User.ROLES)


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': 'autofocus'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'password'
        })
    )
