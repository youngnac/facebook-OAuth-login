import requests
from django.shortcuts import render

from facebook import settings


def post_like_view(request):
    return render(request, 'post/likes.html')


def post_list_view(request):
    APP_ID = settings.config['facebook']['app_id']
    SECRET_CODE = settings.config['facebook']['secret_code']
    REDIRECT_URI = 'http://localhost:8000/post/list/'
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
        dict_access_token = r.json()
        USER_ACCESS_TOKEN = dict_access_token['access_token']

        user = request.user
        url_api_user = 'https://graph.facebook.com/{user_id}'.format(
            user_id=user.username)

        params_2 = {
            'fields': 'posts.limit(50){likes,comments}',
            'access_token': USER_ACCESS_TOKEN,
        }
        r = requests.get(url_api_user, params_2)
        dict_user_info_likes = r.json()

        all_likes = []
        all_comments = []
        user_info = {'all_likes': all_likes, 'all_comments': all_comments}
        for index, post in enumerate(dict_user_info_likes["posts"]["data"]):
            post_id = 'post' + str(index)
            likes_list = []
            comments_list = []
            # pprint(post)
            user_info[post_id] = {'likes': likes_list, 'comments': comments_list}
            # pprint(user_info)
            try:
                for likes in post["likes"]["data"]:
                    likes_list.append(likes["name"])
                    all_likes.append(likes["name"])
            except KeyError:
                continue

            try:
                for comments in post["comments"]["data"]:
                    comments_list.append(comments["from"]["name"])
                    all_comments.append(comments["from"]["name"])
            except KeyError:
                continue

        no_repeat_likes = set(user_info["all_likes"])
        no_repeat_comments = set(user_info["all_comments"])

        likes_count = []
        for i in no_repeat_likes:
            c = user_info["all_likes"].count(i)
            a = {'name': i, 'count': c}
            likes_count.append(a)

        likes_sort_list = sorted(likes_count, key=lambda k: k['count'])

        comments_count = []
        for k in no_repeat_comments:
            b = user_info["all_comments"].count(k)
            g = {'name': k, 'count': b}
            comments_count.append(g)
        comments_sort_list = sorted(comments_count, key=lambda k: k['count'])

        context = {
            'info': user_info,
            'dict_count_likes': likes_sort_list[::-1],
            'dict_count_comments': comments_sort_list[::-1],
        }

        return render(request, 'post/list.html', context)
    context = {
        'facebook_app_id': APP_ID,
    }
    return render(request, 'post/list.html', context)
