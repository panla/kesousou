# -*- encoding=utf-8 -*-

from drf_yasg import openapi

periodical_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='doi or title or first_creator or keywords',
        type=openapi.TYPE_STRING
    )
]

periodical_update_params = openapi.Schema(
    title='periodicals', description='更新periodicals',
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(description='期刊标题', type=openapi.TYPE_STRING),
        'abstract': openapi.Schema(description='期刊简介', type=openapi.TYPE_STRING),
        'publish_date': openapi.Schema(description='发布日期', type=openapi.TYPE_STRING),
        'keywords': openapi.Schema(
            description='关键词', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'creators': openapi.Schema(
            description='作者', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'first_creator': openapi.Schema(description='第一作者', type=openapi.TYPE_STRING),
        'foundations': openapi.Schema(
            description='基金项目', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
    }
)
