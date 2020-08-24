# -*- encoding=utf-8 -*-

from django.urls import re_path, path

from admin.views.user import UserJWTView

app_name = 'admin'
urlpatterns = [
    re_path(r'^api-token/$', UserJWTView.as_view(), name='create_user_token'),
]