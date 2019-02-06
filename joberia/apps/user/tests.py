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

    def test_auth_fails_with_wrong_data(self):
        data = {
            'username': 'mrtn',
            'password': 'hello',
            'platform': '1'
        }
        response = self.client.post(path=self.path, data=json.dumps(data), content_type='application/json')

        print(json.loads(str(response.content, encoding='utf-8')))
