import json
import unittest

from django.test import Client

from joberia.apps.common.test_tools import get_default_user_token, create_default_user, create_default_platform, \
    create_default_job
from joberia.apps.job.models import Job
from joberia.apps.job.serializers import JobSerializer


class CreateJobTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')

    def test_job_gets_created(self):
        path = '/job/'
        job = Job.objects.filter(id=1).first()
        if job is None:
            create_default_job(self.client)

        data = {
            'title': 'Joberia AI Engineer',
            'created_by': '1',
            'description': 'Hello',
            'short_description': 'asdfaf',
            'desired_profile': ['self reliant', 'docker skills', 'aws', '4 years experience'],
            'offers': ['home office', 'high salary', 'budget', 'vacations'],
            'bonuses': [{'salary': '13', 'pets allowed': True}],
            'location_tags': ['munich'],
            'skill_tags': ['postgres', 'docker', 'nodejs', 'react'],
        }

        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_default_user_token()
        }

        response = self.client.post(path=path, data=data, content_type='application/json',
                                    **auth_headers)

        # check that job was created

        jobs = Job.objects.all()
        job = jobs.first()
        self.assertNotEqual(job, None)
        self.assertEqual(job.title, data['title'])
        self.assertEqual(list(job.comments.all()), [])
        self.assertEqual(job.description, data['description'])
        self.assertEqual(job.short_description, data['short_description'])
        self.assertEqual(len(job.desired_profile.all()), len(data['desired_profile']))
        # ...


class GetJobTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')

    def test_returns_whole_list(self):
        job = Job.objects.filter(id=1).first()
        if job is None:
            create_default_job(self.client)

        path = '/job/'
        response = self.client.get(path=path)

        result = json.loads(str(response.content, encoding='utf-8'))

        job = Job.objects.all().first()

        data = JobSerializer(instance=job).data

        self.assertEqual(result[0], data)

    def test_returns_single_eleemnt(self):
        job = Job.objects.filter(id=1).first()
        if job is None:
            create_default_job(self.client)

        path = '/job/?id=1'

        response = self.client.get(path=path)

        result = json.loads(str(response.content, encoding='utf-8'))

        job = Job.objects.filter(pk=1).first()

        data = JobSerializer(instance=job).data

        self.assertEqual(result, data)


class DeleteJobTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')

    def test_deletes_single_eleemnt(self):
        job = Job.objects.filter(id=1).first()
        if job is None:
            create_default_job(self.client)
        path = '/job/?id=1'
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_default_user_token()
        }

        response = self.client.delete(path=path, **auth_headers)

        result = json.loads(str(response.content, encoding='utf-8'))

        self.assertEqual(result, {"success": {"message": "1 was deleted successfully."}})
