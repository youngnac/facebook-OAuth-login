# Create your models here.

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         now = timezone.now()
#         if not email:
#             raise ValueError('The given email must be set')
#         email = CustomUserManager.normalize_email(email)
#         user = self.model(email=email, is_staff=False,
#                           is_active=False, is_superuser=False,
#                           last_login=now, joined_date=now,
#                           is_tutor=False, **extra_fields)
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         super_user = self.create_user(email, password, **extra_fields)
#         super_user.is_staff = True
#         super_user.is_active = True
#         super_user.is_superuser = True
#         super_user.save(using=self._db)
#         return super_user
#
#
# class MyUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=30, blank=False)
#     nickname = models.CharField(max_length=15, blank=True, )
#     cellphone = models.CharField(max_length=11, blank=True)
#     profile_image = models.ImageField(upload_to='member/profile_image',
#                                       blank=True)
#     is_staff = models.BooleanField(default=False,
#                                    help_text='Designates whether the user can log into this admin '
#                                              'site.')
#     is_active = models.BooleanField(default=False,
#                                     help_text='Designates whether this user should be treated as '
#                                               'active. Unselect this instead of deleting accounts.')
#     joined_date = models.DateTimeField(auto_now_add=True)
#     is_tutor = models.BooleanField(default=False)
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = 'name',
#
#     def __str__(self):
#         return self.email
#
#     class Meta:
#         verbose_name = 'user'
#         verbose_name_plural = 'users'
#
#     def get_full_name(self):
#         return self.name
#
#     def get_short_name(self):
#         return self.name
#
#

#
class MyUserManager(UserManager):
    def create_facebook_user(self, facebook_id, user_type='f',
                             email=None, password=None, **extra_fields):
        if not facebook_id:
            raise ValueError('The given facebook id must be set')
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
        return super().create_user(username='FB{}'.format(facebook_id),
                                   user_type=user_type,
                                   email=email, password=password, **extra_fields)


class MyUser(AbstractUser):
    USER_TYPE = (
        ('d', 'Django'),
        ('f', 'Facebook'),
    )
    name = models.CharField(max_length=30, blank=False)
    nickname = models.CharField(max_length=15, blank=True, )
    cellphone = models.CharField(max_length=11, blank=True)
    profile_image = models.ImageField(upload_to='member/profile_image',
                                      blank=True)
    user_type = models.CharField(choices=USER_TYPE, max_length=1, default='d')
    joined_date = models.DateTimeField(auto_now_add=True)
    is_tutor = models.BooleanField(default=False)

    objects = MyUserManager()


