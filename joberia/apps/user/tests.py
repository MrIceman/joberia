import json
import unittest

from django.test import Client

from joberia.apps.common.test_tools import create_default_platform, create_default_user


# Create your tests here.


class RegisterUserViewTest(unittest.TestCase):
    path = '/user/register/'

    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)

    def test_create_user(self):
        response = create_default_user(self.client)

        result = json.loads((str(response.content, encoding='utf-8')))

        self.assertEqual(result['username'], 'django')


class LoginUserViewTest(unittest.TestCase):
    path = '/user/login/'

    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')

    def test_auth_suceeds(self):
        data = {
            'username': 'mrtn',
            'password': 'hello',
            'platform': '1'
        }
        result_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiJtcnRuIiwicGFzc3dvcmRfaGFzaCI6IjJjZjI0ZGJhNWZiMGEzMGUyNmU4M2IyYWM1YjllMjllMWIxNjFlNWMxZmE3NDI1ZTczMDQzMzYyOTM4Yjk4MjQiLCJwbGF0Zm9ybV9pZCI6MX0.6QVF5Rb_nTpZKk9EIcsRPB2IaKGq1hSPjGfNnYHB7NE'

        response = self.client.post(path=self.path, data=json.dumps(data), content_type='application/json')

        result = json.loads(str(response.content, encoding='utf-8'))

        self.assertEqual(result['token'], result_token)


