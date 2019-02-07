from functools import wraps

from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header

from joberia.apps.common import REQUEST_KEY_PLATFORM, REQUEST_KEY_USER
from joberia.apps.user.models import User
from .jwt import decode_jwt_token, USER_ID, PW_HASH, PLATFORM_ID
from .responses import create_auth_invalid_response


def jwt_required(func):
    @wraps(func)
    def auth(request, *args, **kwargs):
        data = get_authorization_header(request).split()
        try:
            payload = decode_jwt_token(data[1])
            user_id, pw_hash, platform = payload[USER_ID], payload[PW_HASH], payload[PLATFORM_ID]

            user = User.objects.filter(pk=user_id).first()

            if user is None:
                return JsonResponse(create_auth_invalid_response('User does not exist.'))
            if user.password != pw_hash:
                return JsonResponse(create_auth_invalid_response('Password is invalid'))
            if user.platform.pk != platform:
                return JsonResponse(create_auth_invalid_response('User does not exist on that Platform'))

            kwargs.update({REQUEST_KEY_PLATFORM: user.platform, REQUEST_KEY_USER: user})
            return func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(
                create_auth_invalid_response('Authentication token is missing or malformed. {}'.format(str(e))))
        pass

    return auth
