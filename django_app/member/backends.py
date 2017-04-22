import os
import re
from tempfile import NamedTemporaryFile

import requests
from django.core.files import File

from member.models import MyUser

class FacebookBackend():
    def authenticate(self, facebook_id, extra_fields=None):
        url_profile = 'https://graph.facebook.com/{user_id}/picture'.format(
            user_id=facebook_id,
        )
        params = {
            'type': 'large',
            'width': '500',
            'height': '500',
        }
        temp_file = NamedTemporaryFile(delete=False)
        r = requests.get(url_profile, params, stream=True)
        _, file_ext = os.path.splitext(r.url)
        # \1은 [^?] 첫번째regex그룹
        file_ext = re.sub(r'(\.[^?]+).*', r'\1', file_ext)
        file_name = '{}{}'.format(
            facebook_id,
            file_ext
        )
        for chunk in r.iter_content(1024):
            temp_file.write(chunk)

        defaults = {
            'first_name': extra_fields.get('first_name', ''),
            'last_name': extra_fields.get('last_name', ''),
        }
        print(defaults)
        print(defaults["email"])
        user, user_created = MyUser.objects.get_or_create(
            username=defaults["facebook_id"],
            name=defaults['last_name']+' '+defaults["first_name"],
        )
        user.profile_image.save(file_name, File(temp_file))

        return user

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None


# class FacebookBackend():
#     def authenticate(self, facebook_id, extra_fields=None):
#         url_profile = 'https://graph.facebook.com/{user_id}/picture'.format(
#             user_id=facebook_id,
#         )
#         params = {
#             'type': 'large',
#             'width': '500',
#             'height': '500',
#         }
#         temp_file = NamedTemporaryFile(delete=False)
#         r = requests.get(url_profile, params, stream=True)
#         _, file_ext = os.path.splitext(r.url)
#         # \1은 [^?] 첫번째regex그룹
#         file_ext = re.sub(r'(\.[^?]+).*', r'\1', file_ext)
#         file_name = '{}{}'.format(
#             facebook_id,
#             file_ext
#         )
#         for chunk in r.iter_content(1024):
#             temp_file.write(chunk)
#
#         defaults = {
#             'first_name': extra_fields.get('first_name', ''),
#             'last_name': extra_fields.get('last_name', ''),
#             'email': extra_fields.get('email', ''),
#         }
#         print(defaults)
#         print(defaults["email"])
#         user, user_created = MyUser.objects.get_or_create(
#             email=defaults["email"],
#             name=defaults['first_name']+defaults["last_name"],
#
#         )
#         user.profile_image.save(file_name, File(temp_file))
#
#         return user
#
#     def get_user(self, user_id):
#         try:
#             return MyUser.objects.get(id=user_id)
#         except MyUser.DoesNotExist:
#             return None
