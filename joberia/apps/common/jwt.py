import os

import jwt

USER_ID = 'userid'
PW_HASH = 'password_hash'
PLATFORM_ID = 'platform_id'


def encode_jwt_token(username, password_hash, platform_id):
    token = jwt.encode({USER_ID: username, PW_HASH: password_hash, PLATFORM_ID: platform_id},
                       key=os.environ.get('JWT_KEY'), algorithm='HS256')
    return token


def decode_jwt_token(jwt_token):
    try:
        token = jwt.decode(jwt_token, key=os.environ.get('JWT_KEY'), algorithms=['HS256'])
        return token
    except jwt.exceptions.DecodeError:
        return False


def validate_jwt_token(jwt_token, username, password_hash, platform_id):
    try:
        token = jwt.decode(jwt_token, key=os.environ.get('JWT_KEY'), algorithms=['HS256'])
        return token.get(USER_ID, None) == username and token.get(PW_HASH,
                                                                  None) == password_hash and token.get(PLATFORM_ID,
                                                                                                        None) == platform_id
    except jwt.exceptions.DecodeError:
        return False
