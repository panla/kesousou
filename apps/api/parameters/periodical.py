# -*- encoding=utf-8 -*-

from drf_yasg import openapi

periodical_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='doi or title or first_creator or periodical_name or foundations or abstract or keywords',
        type=openapi.TYPE_STRING
    )
]
