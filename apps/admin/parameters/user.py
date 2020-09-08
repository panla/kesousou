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

# 请求接口时，HEADERS 参数
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
    'is_superuser': openapi.Schema(description='是否是管理员', type=openapi.TYPE_BOOLEAN),
    'is_active': openapi.Schema(description='是否有效', type=openapi.TYPE_BOOLEAN),
}

user_create_parameters = openapi.Schema(
    title='user', description='创建user', type=openapi.TYPE_OBJECT,
    properties=user_properties,
    required=['password']
)

user_update_parameters = openapi.Schema(
    title='user', description='更新user', type=openapi.TYPE_OBJECT,
    properties=user_properties,
)

user_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY, description='username or mobile or email',
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        name='is_superuser', in_=openapi.IN_QUERY, description='is_superuser',
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        name='is_active', in_=openapi.IN_QUERY, description='is_active',
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        name='order', in_=openapi.IN_QUERY, description='order param',
        type=openapi.TYPE_STRING
    )
]
