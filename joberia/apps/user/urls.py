from django.urls import path
from django.views.generic import TemplateView

from joberia.apps.user.views import (
    Login, Register, PasswordForgot, PasswordReset, Logout
)

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),

    path('password_forgot/', PasswordForgot.as_view(), name='password_forgot'),

    path(
        'password_forgot/link_took_off/',
        TemplateView.as_view(template_name='request_password_reset_success.html'),
        name='password_forgot_success'
    ),

    path('password_forgot/reset/<str:onetime_hash>/', PasswordReset.as_view(), name='password_reset'),

]
