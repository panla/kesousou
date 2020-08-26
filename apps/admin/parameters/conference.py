# -*- encoding=utf-8 -*-

from drf_yasg import openapi

conference_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='title or first_creator or keywords',
        type=openapi.TYPE_STRING
    ),
]

conference_update_params = openapi.Schema(
    title='conference', description='更新conference',
    type=openapi.TYPE_OBJECT,
    properties={
        'abstract': openapi.Schema(description='论文摘要', type=openapi.TYPE_STRING),
        'keywords': openapi.Schema(
            description='关键词', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'creators': openapi.Schema(
            description='作者', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'first_creator': openapi.Schema(description='第一作者', type=openapi.TYPE_STRING),
        'sponsors': openapi.Schema(
            description='主办单位', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'experts': openapi.Schema(
            description='关联专家id', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER)
        ),
    }
)