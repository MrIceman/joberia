from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from joberia.apps.user.views import (
    Login, Register, ProfileView, confirm_register, PasswordForgot, PasswordReset
)


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),

    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('register/confirm/<str:confirm_hash>/', confirm_register, name='confirm_register'),


    path('password_forgot/', PasswordForgot.as_view(), name='password_forgot'),

    path(
        'password_forgot/link_took_off/',
        TemplateView.as_view(template_name='request_password_reset_success.html'),
        name='password_forgot_success'
    ),

    path('password_forgot/reset/<str:onetime_hash>/', PasswordReset.as_view(), name='password_reset'),

]
