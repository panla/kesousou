# -*- encoding=utf-8 -*-

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

class PagePagination(PageNumberPagination):
    """ 自定义分页"""
    page_size = 5
    page_size_query_param = "size"
    page_query_param = "page"


def get_results(request, queryset, view, serializer_class):
    paginator = PagePagination()
    data = paginator.paginate_queryset(queryset, request, view)
    data = serializer_class(data, many=True, context={'request': request}).data
    return data
