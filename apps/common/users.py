from django.db.models import Q
from django.contrib.auth.views import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.permissions import BasePermission

User = get_user_model()


def authenticate(username=None, password=None, **kwargs):
    """
    用户认证，根据邮箱或手机号以及密码完成认证
    """
    try:
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        user = User.objects.get(Q(email=username) | Q(mobile=username))
        if user.check_password(password):
            return user
    except Exception as exc:
        return None


class IsAdminUser(BasePermission):
    """自定义判断是否是管理员的 permission_class"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class UserBackend(ModelBackend):
    """ 自定义用户认证，在 settings 通过 AUTHENTICATION_BACKENDS 指定"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        return authenticate(username, password, **kwargs)
