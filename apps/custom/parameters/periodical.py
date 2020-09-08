# -*- encoding=utf-8 -*-

from drf_yasg import openapi

periodical_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='doi or title or first_creator or keywords',
        type=openapi.TYPE_STRING
    )
]
