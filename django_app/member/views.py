from pprint import pprint

import requests
from django.shortcuts import render

from facebook import settings


def login_view(request):
    facebook_app_id = settings.config['facebook']['app_id']
    context = {
        'facebook_app_id': facebook_app_id

    }
    return render(request, 'member/login.html', context)


def login_facebook(request):
    APP_ID = settings.config['facebook']['app_id']
    SECRET_CODE = settings.config['facebook']['secret_code']
    REDIRECT_URI = 'http://localhost:8000/member/login/facebook/'
    APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE)
    if request.GET.get('code'):
        code = request.GET.get('code')
        url_request_access_token = "https://graph.facebook.com/v2.8/oauth/access_token"
        params = {
            'client_id': APP_ID,
            'client_secret': SECRET_CODE,
            'code': code,
            'redirect_uri': REDIRECT_URI,
        }
        r = requests.get(url_request_access_token, params=params)
        dict_access_token = r.json()
        USER_ACCESS_TOKEN = dict_access_token['']
        print('ACCESS_TOKEN : %s' % USER_ACCESS_TOKEN)

        url_debug_token = 'https://graph.facebook.com/debug_token'
        params = {
            'input_token': USER_ACCESS_TOKEN,
            'access_token': APP_ACCESS_TOKEN,
        }
        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.json()
        pprint(dict_debug_token)
        USER_ID = dict_debug_token['data']['user_id']
        print('USER_ID : %s' % USER_ID)
