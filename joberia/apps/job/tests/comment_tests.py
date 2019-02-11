import json
import unittest

from django.test import Client

from joberia.apps.common.test_tools import get_default_user_token, create_default_user, create_default_platform, \
    create_default_job, create_default_comment


class CreateCommentTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')
        create_default_job(self.client)

    def test_creates_comment(self):
        data = {
            'text': 'Are you hiring?',
            'job_id': '1',
        }

        path = '/job/comment'
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_default_user_token()
        }

        response = self.client.post(path=path, data=data,
                                    content_type='application/json', **auth_headers)

        self.assertEqual(json.loads(str(response.content, encoding='utf-8'))['text'], 'Are you hiring?')

    def test_gets_job_with_comments(self):
        create_default_comment(self.client)
        result = self.client.get('/job?id=1&platform=1')
        data = json.loads(str(result.content, encoding='utf-8'))
        self.assertEqual(len(data['comments']), 2)


class EditCommentTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')
        create_default_job(self.client)
        create_default_comment(self.client)

    def test_comment_gets_edited(self):
        data = {
            'author': '1',
            'text': 'Hula Hula Hup',
            'job': '1',
            'id': '1'
        }

        path = '/job/comment'
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_default_user_token()
        }

        response = self.client.put(path=path, data=data,
                                   content_type='application/json', **auth_headers)

        response_data = json.loads(str(response.content, encoding='utf-8'))
        self.assertEqual(response_data['text'], data['text'])


class DeleteCommentTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')
        create_default_job(self.client)

    def test_comment_gets_edited(self):
        comment = create_default_comment(self.client, text='Born to be deleted.')
        path = '/job/comment?id={comment_id}&?job={job_id}'.format(job_id='1', comment_id=comment['id'])
        auth_headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + get_default_user_token()
        }

        response = self.client.delete(path=path, **auth_headers)
        response_data = json.loads(str(response.content, encoding='utf-8'))
    #  self.assertEqual(response_data,
    #                   {"success": {"message": "Comment {} was deleted successfully.".format(comment['id'])}})


class GetCommandTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        create_default_platform(self.client)
        create_default_user(self.client, 'mrtn', 'mrtnnwsd@gmail.com', password='hello')
        create_default_job(self.client)

    def test_gets_comment_list(self):
        path = '/job?=platform=1/{job_id}/comment'
        response = self.client.get(path=path)

    #  print('Response: {}'.format(response.content))
