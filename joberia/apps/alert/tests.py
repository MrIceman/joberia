"""import json

from joberia.apps.user.models import User
from django.test import TestCase, RequestFactory
from joberia.apps.alert.models import Alert
from joberia.apps.alert.views import DeveloperAlerts


class DevAlertTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        mrtn = {
            'email': 'mrtnnwsd@gmail.com',
            'username': 'mrtn'}
        doni = {
            'email': 'dnjrbv@gmail.com',
            'username': 'doni',
            'id': 120
        }
        cls.usr_1 = User.objects.create(username=mrtn['username'], email=mrtn['email'], password='abcdefgh')
        cls.usr_2 = User.objects.create(username=doni['username'], email=doni['email'], password='abcdefgh', id=120)

        cls.a_1 = Alert.objects.create(user=cls.usr_1, type='dev', )
        cls.a_2 = Alert.objects.create(user=cls.usr_2, type='dev', )

    def test_get_dev_endpoint_returns_doni_and_martin(self):
        request = self.factory.get('/alert/dev')

        response = DeveloperAlerts.as_view()(request)
        result = json.loads(response.content)
        self.assertEqual(result, [{
            'id': 1,
            'user_id': 1,
            'type': 'dev',
            'active': True
        },
            {
                'id': 2,
                'user_id': 120,
                'type': 'dev',
                'active': True
            },
        ])

    def test_get_dev_with_id_returns_user(self):
        request = self.factory.get('/alert/dev?id=120')

        response = DeveloperAlerts.as_view()(request)
        result = json.loads(response.content)
        self.assertEqual(result, {
            'id': 2,
            'user_id': 120,
            'type': 'dev',
            'active': True
        })

    def test_post_returns_new_alert(self):
        usr_3 = User.objects.create(username='jondoe', email='jondoe@gmail.com')
        request_data = {
            'user_id': usr_3.pk,
            'type': 'dev',
            'is_active': True
        }
        request = self.factory.post('/alert/dev', data=json.dumps(request_data), content_type='Application/Json')
        response = DeveloperAlerts.as_view()(request)

        self.assertEqual(json.loads(response.content), {
            'id': 3,
            'user_id': usr_3.pk,
            'type': 'dev',
            'active': True
        })
"""""