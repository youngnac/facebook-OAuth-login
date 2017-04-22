from django.conf.urls import url

from post import views


app_name = "post"
urlpatterns = [
    url(r'^likes/$', views.post_like_view, name="post_likes"),
    url(r'^list/$', views.post_list_view, name="post_list")
]