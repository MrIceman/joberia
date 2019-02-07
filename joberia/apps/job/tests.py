import time
import unittest

from django.test import Client

from joberia.apps.common.test_tools import get_default_user_token, create_default_user, create_default_platform


class CreateJobViewTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')


    def test_job_gets_created(self):
        path = '/job/create/'
        data = {
            'title': 'Joberia AI Engineer',
            'created_by': '1',
            'description': 'Hello',
            'short_description': 'asdfaf',
            'desired_profile': ['4 years experience', 'aws', 'docker skills', 'self reliant'],
            'offers': ['home office', 'high salary', 'budget', 'vacations'],
            'bonuses': [{'salary': '13', 'pets allowed': True}],
            'location_tags': ['munich'],
            'skill_tags': ['postgres', 'docker', 'nodejs', 'react'],
            'expires_at': time.time(),
        }

        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_default_user_token()
        }

        response = self.client.post(path=path, data=data, content_type='application/json',
                                    **auth_headers)

        print('Received response: {}'.format(response.content))
