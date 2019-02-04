import json
import unittest

from django.test import Client


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

        response = self.client.post('/spawner/platform/', data=json.dumps(data),
                                    content_type='application/json')

        print(str(response.content, encoding='UTF-8'))

