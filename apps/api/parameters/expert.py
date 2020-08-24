# -*- encoding=utf-8 -*-

from drf_yasg import openapi

expert_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='name or organization or major or research_areas personal_introduction or keywords',
        type=openapi.TYPE_STRING
    ),
]
