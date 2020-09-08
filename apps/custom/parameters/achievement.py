from drf_yasg import openapi

achievement_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='sn or title or keywords or organizations or creators',
        type=openapi.TYPE_STRING
    ),
]
