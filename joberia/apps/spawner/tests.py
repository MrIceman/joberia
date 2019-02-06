import json
import unittest

from django.test import Client

from joberia.apps.spawner.models import Platform
from joberia.apps.utils.responses import create_data_does_not_exist_error


class CreatePlatformTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_creates_platform(self):
        data = {
            'platform_name': 'joberia_default',
            'home_text_header': 'Joberia.ai Jobs!',
            'home_text_sub_header': 'Find Joberia experts in your area',
            'description': 'some blabla and more blablabla',
            'home_text_body': 'more and more bla bla bla',
            'footer_text': 'good bye blablabla'
        }

        _response = self.client.post('/spawner/platform/', data=json.dumps(data),
                                     content_type='application/json')

        test = Platform.objects.all()

        self.assertEqual(len(test), 1)

    def test_gets_created_platform(self):
        response = self.client.get('/spawner/platform/?platform_id=1')

        obj = json.loads(str(response.content, encoding='utf-8'))

        self.assertEqual(obj['id'], 1)
        self.assertEqual(obj['platform_name'], 'joberia_default')

    def test_gets_error_message_because_item_does_not_exist(self):
        response = self.client.get('/spawner/platform/?platform_id=14')

        obj = json.loads(str(response.content, encoding='utf-8'))

        self.assertEqual(obj, create_data_does_not_exist_error())

    def test_returns_array_of_items_when_no_id_attached(self):
        response = self.client.get('/spawner/platform/')

        obj = json.loads(str(response.content, encoding='utf-8'))

        print(obj)
