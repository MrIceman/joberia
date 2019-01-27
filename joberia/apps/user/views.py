from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views.generic import FormView, View

from joberia.apps.core.models import create_default_hash
from joberia.apps.core.utils import send_email_in_template
from joberia.apps.spawner.models import Theme
from joberia.apps.user.models import User
from .forms import LoginForm, RegisterForm


class Logout(View):

    def get(self, request):
        logout(request)
        return render(request, 'index.html')


class Login(FormView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {
            'login_form': LoginForm(), 'register_form': RegisterForm()
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme = Theme.objects.filter().all().first()
        context['theme'] = theme
        return context

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST or None)

        if login_form.is_valid():
            data = login_form.cleaned_data
            username = data.get('username')
            password = data.get('password')

            if '@' in username:
                user_model = get_user_model()
                try:
                    user = user_model.objects.get(email=username)
                    if user is None:
                        return render(request, 'login.html', {
                            'login_form': login_form,
                            'login_error': 'Email does not exist'
                        })
                    else:
                        if user.check_password(password):
                            login(request, user)
                            return redirect(reverse('panel'))
                except:
                    return render(request, 'login.html', {
                        'login_form': login_form,
                        'login_error': 'Email {} does not exist in our database'.format(username)
                    })

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('panel'))
                else:
                    # user is not active, user should confirm his registration first
                    return render(request, 'index.html', {
                        'login_form': login_form, 'register_form': RegisterForm(),
                        'login_error': 'Please confirm your registration.'
                    })
            else:
                # bad credentials
                return render(request, 'login.html', {
                    'login_form': login_form, 'register_form': RegisterForm(),
                    'login_error': 'Wrong credentials'
                })

        # bad form data
        return render(request, 'login.html', {
            'login_form': login_form, 'register_form': RegisterForm(),
            'login_error': 'Wrong credentials'
        })


class Register(FormView):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html', {
            'register_form': RegisterForm()
        })

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('new_username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            role = form.cleaned_data.get('role')

            if password2 != password1:
                return render(request, 'register.html', {
                    'register_form': RegisterForm(),
                    'register_form': form,
                    'reg_error': 'Passwords don\'t match'
                })

            if User.objects.filter(email=email).count():
                return render(request, 'login.html', {
                    'login_form': LoginForm(),
                    'register_form': form,
                    'reg_error': 'User with this email exists already. Please sign in instead.'
                })

            new_user = User.objects.create(username=username, email=email, is_active=True, role=role)  # debug mode
            new_user.set_password(password2)
            new_user.save()
            return redirect(request, 'login.html', {
                'message': 'You have successfully signed up! Use your email address {email} or {username} to signup.'.format(
                    email=email, username=username
                )})


"""
            # send confirmation link
            confirm_hash = create_default_hash()

            new_user.confirm_hash = confirm_hash
            new_user.save()

            confirm_link = 'https://%s%s' % (
                request.META.get('HTTP_HOST'),
                reverse('confirm_register', kwargs={'confirm_hash': confirm_hash})
            )

            send_email_in_template(
                'Your registration in joberia.com',
                email,
                'email/template.html',
                **{
                    'text': "Thanks for registering on joberon.com. Please confirm your registration by clicking on "
                            "the link below.",
                    'link': confirm_link,
                    'link_name': 'Confirm'
                }
            )
"""


def confirm_register(request, confirm_hash):
    user_profile = User.objects.filter(confirm_hash=confirm_hash).last()

    if not user_profile:
        # either hash is already used or invalid hash
        return redirect('%s?invalid_link=1' % reverse('login'))

    user = user_profile

    if user.is_active:
        return redirect('%s?already_confirmed=1' % reverse('profile'))

    user.is_active = True
    user.save(update_fields=['is_active'])

    # login user
    login(request, user)

    return redirect('%s?registration_complete=1' % reverse('profile'))


class UserView(LoginRequiredMixin, FormView):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html')


class PasswordForgot(FormView):
    def get(self, request, *args, **kwargs):
        return render(request, 'request_password_reset.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        if not email:
            return render(request, 'request_password_reset.html', {
                'error_no_input': 'yes', 'email': email
            })

        if not User.objects.filter(email=email).count():
            return render(request, 'request_password_reset.html', {
                'error_user_not_found': 'yes', 'email': email
            })

        user = User.objects.filter(email=email).last()

        pw_onetime_hash = create_default_hash()
        user.pw_onetime_hash = pw_onetime_hash
        user.save()

        send_email_in_template(
            'your new access',
            email,
            'email/pw_reset.html',
            **{
                'request_domain': request.META.get('HTTP_HOST'),
                'user_name': user.username,
                'pw_reset_url': 'https://%s%s' % (
                    request.META.get('HTTP_HOST'),
                    reverse('password_reset', kwargs={'onetime_hash': pw_onetime_hash})
                ),
            }
        )
        return redirect(reverse('password_forgot_success'))


class PasswordReset(FormView):

    def get(self, request, *args, **kwargs):
        onetime_hash = kwargs.get('onetime_hash')

        user_profile = User.objects.filter(pw_onetime_hash=onetime_hash).last()
        if not user_profile:
            error = 'link is invalid'
            return render(request, 'password_reset.html', {
                'error': error, 'link_invalid': 'yes'
            })

        # invalidate the confirm hash
        now = timezone.now()
        user_profile.pw_onetime_hash = '%s-clicked-at-%s' % (
            onetime_hash, '%s_%s_%s_%s_%s' % (now.year, now.month, now.day, now.hour, now.minute)
        )
        user_profile.save()

        return render(request, 'password_reset.html', {
            'user_profile_id': user_profile.id
        })

    def post(self, request, *args, **kwargs):
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_profile_id = request.POST.get('user_profile_id')

        if not User.objects.filter(id=user_profile_id).last():
            return render(request, 'password_reset.html', {
                'error': 'error while resetting'
            })

        if password1 != password1:
            return render(request, 'password_reset.html', {
                'error': 'passwords dont match'
            })

        user_profile = User.objects.get(id=user_profile_id)
        user = user_profile.user
        user.set_password(password2)
        user.save()

        login(request, user)

        return redirect('%s?password_changed=1' % reverse('profile'))
