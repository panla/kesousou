# -*- encoding=utf-8 -*-

from drf_yasg import openapi

achievement_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='sn or title or organizations or creators or keywords or abstract',
        type=openapi.TYPE_STRING
    )
]