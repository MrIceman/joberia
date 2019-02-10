import json

created_user = False
created_platform = False


def create_default_platform(client):
    global created_platform
    if created_platform:
        return

    data = {
        'platform_name': 'joberia_default',
        'home_text_header': 'Joberia.ai Jobs!',
        'home_text_sub_header': 'Find Joberia experts in your area',
        'description': 'some blabla and more blablabla',
        'home_text_body': 'more and more bla bla bla',
        'footer_text': 'good bye blablabla'
    }

    response = client.post('/spawner/platform/', data=json.dumps(data),
                           content_type='application/json')
    created_platform = True
    return response


def create_default_user(client, username='django', email='django@gmail.com', password='123', platform='1'):
    data = {
        'username': username,
        'email': email,
        'first_name': 'martin',
        'last_name': 'nowosad',
        'platform': platform,
        'role': 'dev',
        'password': password
    }
    response = client.post(path='/user/register/', data=json.dumps(data), content_type='application/json')
    created_user = True
    return response


def create_default_job(client):
    path = '/job/'
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

    response = client.post(path=path, data=data, content_type='application/json',
                           **auth_headers)


def get_default_user_token():
    return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJwYXNzd29yZF9oYXNoIjoiMmNmMjRkYmE1ZmIwYTMwZTI2ZTgzYjJhYzViOWUyOWUxYjE2MWU1YzFmYTc0MjVlNzMwNDMzNjI5MzhiOTgyNCIsInBsYXRmb3JtX2lkIjoxfQ.DWwfIdkPy34nrOY6joejjD_AoaJRqtaiOYA1qJNMTHU'
