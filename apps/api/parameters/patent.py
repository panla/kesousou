# -*- encoding=utf-8 -*-

from drf_yasg import openapi

patent_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='name or abstract or inventors',
        type=openapi.TYPE_STRING,
    ),
]
