# -*- encoding=utf-8 -*-

from django.db.models import Q
from django.contrib.auth.views import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


def authenticate(username=None, password=None, **kwargs):
    try:
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        user = User.objects.get(Q(email=username) | Q(mobile=username))
        if user.check_password(password):
            return user
    except Exception as exc:
        return None


class UserBackend(ModelBackend):
    """ 自定义用户认证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        return authenticate(username, password, **kwargs)
