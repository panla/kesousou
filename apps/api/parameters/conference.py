# -*- encoding=utf-8 -*-

from drf_yasg import openapi

conference_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='title or abstract or first_creator or meeting_title or keywords',
        type=openapi.TYPE_STRING
    ),
]
