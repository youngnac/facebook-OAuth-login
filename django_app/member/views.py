import requests
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from facebook import settings


def login_view(request):
    facebook_app_id = settings.config['facebook']['app_id']
    context = {
        'facebook_app_id': facebook_app_id,
    }

    return render(request, 'member/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def login_facebook(request):
    APP_ID = settings.config['facebook']['app_id']
    SECRET_CODE = settings.config['facebook']['secret_code']
    REDIRECT_URI = 'http://localhost:8000/member/login/facebook/'
    APP_ACCESS_TOKEN = '{app_id}|{secret_code}'.format(
        app_id=APP_ID,
        secret_code=SECRET_CODE
    )

    if request.GET.get('code'):
        code = request.GET.get('code')
        url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token'
        params = {
            'client_id': APP_ID,
            'redirect_uri': REDIRECT_URI,
            'client_secret': SECRET_CODE,
            'code': code,
        }
        r = requests.get(url_request_access_token, params=params)
        print(r.url)
        dict_access_token = r.json()
        USER_ACCESS_TOKEN = dict_access_token['access_token']

        url_debug_token = 'https://graph.facebook.com/debug_token'
        params = {
            'input_token': USER_ACCESS_TOKEN,
            'access_token': APP_ACCESS_TOKEN,
        }
        r = requests.get(url_debug_token, params=params)
        dict_debug_token = r.json()
        USER_ID = dict_debug_token['data']['user_id']

        # 해당 USER_ID로 graph API에 유저정보를 요청
        url_api_user = 'https://graph.facebook.com/{user_id}'.format(
            user_id=USER_ID
        )
        fields = [
            'id',
            'name',
            'gender',
            'picture',
            'email',

        ]
        params = {
            'fields': ','.join(fields),
            'access_token': USER_ACCESS_TOKEN,
        }
        r = requests.get(url_api_user, params)
        print(r.url)
        dict_user_info = r.json()
        print(dict_user_info)
        user = authenticate(facebook_id=USER_ID, extra_fields=dict_user_info)
        login(request, user)
        print(user)
        token = Token.objects.get_or_create(user=user)
        print("AsdfASDFasdfsdfsdfsaf")
        print(token)
    return redirect('index')
