from drf_yasg import openapi

achievement_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='sn or title or keywords or organizations or creators',
        type=openapi.TYPE_STRING
    ),
]

achievement_update_params = openapi.Schema(
    title='achievement', description='更新achievement',
    type=openapi.TYPE_OBJECT,
    properties={
        'organizations': openapi.Schema(
            description='完成单位', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'creators': openapi.Schema(
            description='完成人', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'published_year': openapi.Schema(description='公布年份', type=openapi.TYPE_STRING),
        'keywords': openapi.Schema(
            description='关键词', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'abstract': openapi.Schema(description='简介', type=openapi.TYPE_STRING),
        'province': openapi.Schema(description='省市', type=openapi.TYPE_STRING),
        'trade_name': openapi.Schema(
            description='应用行业名称', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'level': openapi.Schema(description='成果水平', type=openapi.TYPE_STRING),
        'contact_unit': openapi.Schema(description='联系单位', type=openapi.TYPE_STRING),
        'contact_address': openapi.Schema(description='联系单位地址', type=openapi.TYPE_STRING),
        'experts': openapi.Schema(
            description='关联专家id', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER)
        ),
    }
)
