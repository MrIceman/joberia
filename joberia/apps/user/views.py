import json
import time

from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.views.generic import FormView, View
from rest_framework.parsers import JSONParser

from joberia.apps.common.hasher import hash_sha256
from joberia.apps.common.jwt import encode_jwt_token
from joberia.apps.common.responses import register_failed_message, create_auth_invalid_response, \
    create_user_does_not_exist_response, create_password_is_wrong_response, \
    create_platform_does_not_exist_response
from joberia.apps.core.models import create_default_hash
from joberia.apps.core.utils import send_email_in_template
from joberia.apps.user.models import User
from joberia.apps.user.serializers import AuthUserSerializer


class Logout(View):

    def get(self, request):
        logout(request)
        return render(request, 'index.html')


class Login(View):

    def post(self, request):
        try:
            data = json.loads(str(request.body, encoding='utf-8'))
            user = User.objects.filter(username=data['username']).first()

            if user is None:
                return JsonResponse(create_user_does_not_exist_response())
            hashed_password = hash_sha256(data['password'])
            if str(user.password) != str(hashed_password):
                return JsonResponse(create_password_is_wrong_response())
            if int(data['platform']) != user.platform.id:
                return JsonResponse(create_platform_does_not_exist_response())
            token = encode_jwt_token(user.username, user.password, user.platform.id)
            return JsonResponse({'token': str(token, encoding='utf-8')})
        except Exception as e:
            return JsonResponse(create_auth_invalid_response('Login Failed. Reason: {}'.format(str(e))))


class Register(View):

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = AuthUserSerializer(data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.disabled = True
            instance.password = hash_sha256(instance.password)
            instance.confirm_hash = hash_sha256(str(time.time()))
            instance.save()
            token = encode_jwt_token(instance.username, instance.password, instance.platform.id)
            response = serializer.data

            response.update({'jwt': str(token, encoding='utf-8')})
            return JsonResponse(response)
        else:
            return JsonResponse(register_failed_message(serializer.errors))


def confirm_register(request, confirm_hash):
    pass


class PasswordForgot(FormView):
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
