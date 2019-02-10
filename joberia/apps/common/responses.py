def create_data_does_not_exist_response():
    return __template_error_response('Item does not exist.')


def create_user_does_not_exist_response():
    return __template_error_response('User does not exist.')


def create_password_is_wrong_response():
    return __template_error_response('Password is wrong.')


def create_platform_does_not_exist_response():
    return __template_error_response('User does not exist on Platform.')


def create_auth_invalid_response(message=None):
    if message is None:
        message = 'Authentication token is invalid or missing.'
    return __template_error_response(message)


def create_not_authorized_response():
    return __template_error_response('Not authorized to perform action.')


def create_login_successful_response():
    return __template_success_response('Logged in.')


def create_action_successful_response(message):
    return __template_success_response(message)


def register_failed_message(message=None):
    return __template_error_response('Failed to create Account. {}'.format(message))


def create_failed_message(message=None):
    return __template_error_response('Creation Failed' if not message else message)


def __template_error_response(message):
    return {'error': {'message': message}}


def __template_success_response(message):
    return {'success': {'message': message}}
