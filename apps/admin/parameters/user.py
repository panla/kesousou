# -*- encoding=utf-8 -*-

from drf_yasg import openapi

# 获得token的所需参数
create_token_body = openapi.Schema(
    title='params', description='create token', type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(description='邮箱或手机号', type=openapi.TYPE_STRING),
        'password': openapi.Schema(description='密码', type=openapi.TYPE_STRING)
    },
    required=['username', 'password']
)

# 获得token后的返回值
create_token_response = openapi.Schema(
    title='token', description='token', type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(description='user_id', type=openapi.TYPE_INTEGER),
        'token': openapi.Schema(description='token', type=openapi.TYPE_STRING)
    }
)

token_parameters = [
    openapi.Parameter(
        name='Authorization', in_=openapi.IN_HEADER, description='Token token',
        required=True, type=openapi.TYPE_STRING
    )
]

user_properties = {
    'username': openapi.Schema(description='用户名', type=openapi.TYPE_STRING),
    'email': openapi.Schema(description='邮箱', type=openapi.TYPE_STRING),
    'mobile': openapi.Schema(description='手机号', type=openapi.TYPE_STRING),
    'password': openapi.Schema(description='密码', type=openapi.TYPE_STRING),
}

create_user_parameters = openapi.Schema(
    title='params', description='创建一个用户', type=openapi.TYPE_OBJECT,
    properties=user_properties, required=['password']
)
