# -*- encoding=utf-8 -*-

from drf_yasg import openapi

patent_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='name or inventors or patent_code or publication_number',
        type=openapi.TYPE_STRING,
    ),
]
