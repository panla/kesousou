from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi

# 分页参数
page_params = [
    openapi.Parameter(
        name='page', in_=openapi.IN_QUERY, description='page-number',
        type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        name='size', in_=openapi.IN_QUERY, description='page-size',
        type=openapi.TYPE_INTEGER
    )
]


class PagePagination(PageNumberPagination):
    """ 自定义分页，每页5条数据"""
    page_size = 5
    page_size_query_param = "size"
    page_query_param = "page"


def get_results(request, queryset, view, serializer_class):
    """
    返回分页后的结果
    """
    paginator = PagePagination()
    data = paginator.paginate_queryset(queryset, request, view)
    data = serializer_class(data, many=True, context={'request': request}).data
    return data
