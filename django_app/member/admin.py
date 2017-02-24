from django.contrib import admin

# Register your models here.
from member.models import MyUser


admin.site.register(MyUser)