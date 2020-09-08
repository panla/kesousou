from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results, page_params
from common.order import order_params
from model.models import Expert
from custom.parameters.expert import expert_filter_params
from custom.serializers.expert import ExpertListSerializer, ExpertDetailSerializer


class ExpertListView(APIView):
    @swagger_auto_schema(
        manual_parameters=expert_filter_params + order_params + page_params, operation_id='expert_list',
        responses={200: ExpertListSerializer(many=True)}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        """
        专家列表，
        查询字段 text，排序参数 order
        模糊查询字段包括 major, research_areas, keywords
        精准查询字段包括 name, organization
        """
        text = request.query_params.get('text')
        order = request.query_params.get('order')
        queryset = Expert.objects.all()
        if text:
            queryset = queryset.filter(
                Q(name=text) | Q(organization=text) | Q(major__contains=text) | Q(research_areas__contains=text)
                | Q(keywords__contains=text)
            )
        if order:
            queryset = queryset.order_by(order)
        data = get_results(request, queryset, self, ExpertListSerializer)
        return Response({'count': queryset.count(), 'experts': data}, status.HTTP_200_OK)


class ExpertDetailView(generics.RetrieveAPIView):
    serializer_class = ExpertDetailSerializer
    queryset = Expert.objects.all()

    @swagger_auto_schema(
        operation_id='expert_read', responses={200: ExpertDetailSerializer()}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        """
        专家详情
        """
        return self.retrieve(request, *args, **kwargs)
