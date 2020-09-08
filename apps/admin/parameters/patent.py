from drf_yasg import openapi

patent_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='name or inventors or patent_code or publication_number',
        type=openapi.TYPE_STRING,
    ),
]

patent_update_params = openapi.Schema(
    title='patent', description='更新patent',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(description='专利名称', type=openapi.TYPE_STRING),
        'abstract': openapi.Schema(description='专利简介', type=openapi.TYPE_STRING),
        'patent_type': openapi.Schema(description='专利类型', type=openapi.TYPE_STRING),
        'patent_code': openapi.Schema(description='专利申请号', type=openapi.TYPE_STRING),
        'application_date': openapi.Schema(description='专利申请日期', type=openapi.TYPE_STRING),
        'publication_number': openapi.Schema(description='专利公开号', type=openapi.TYPE_STRING),
        'publication_date': openapi.Schema(description='专利公告日期', type=openapi.TYPE_STRING),
        'applicants': openapi.Schema(
            description='申请人', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'inventors': openapi.Schema(
            description='发明人', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        'claim': openapi.Schema(description='主权项', type=openapi.TYPE_STRING),
        'legal_status': openapi.Schema(description='法律状态', type=openapi.TYPE_STRING),
        'experts': openapi.Schema(
            description='关联专家id', type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER)
        ),
    }
)
