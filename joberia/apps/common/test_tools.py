import json


def create_default_platform(client):
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

    return response
