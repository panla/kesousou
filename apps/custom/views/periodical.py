from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results, page_params
from common.order import order_params
from model.models import Expert, Periodical
from custom.serializers.periodical import PeriodicalListSerializer, PeriodicalDetailSerializer
from custom.parameters.periodical import periodical_filter_params


class PeriodicalsView(APIView):
    @swagger_auto_schema(
        manual_parameters=periodical_filter_params + order_params + page_params, operation_id='periodical_list',
        responses={200: PeriodicalListSerializer(many=True)}, tags=['periodicals']
    )
    def get(self, request, *args, **kwargs):
        """
        查看期刊列表，
        查询参数 text，排序参数 order
        模糊查询字段包括 title, keywords
        精准查询字段包括 doi, first_creator
        """
        text = request.query_params.get('text')
        order = request.query_params.get('order')
        queryset = Periodical.objects.all()
        if text:
            queryset = queryset.filter(
                Q(doi=text) | Q(title__contains=text) | Q(first_creator=text) | Q(keywords__contains=text)
            )
        if order:
            queryset = queryset.order_by(order)
        data = get_results(request, queryset, self, PeriodicalDetailSerializer)
        return Response({'count': queryset.count(), 'periodicals': data}, status.HTTP_200_OK)


class ExpertPeriodicalsView(APIView):
    @swagger_auto_schema(
        manual_parameters=order_params + page_params, operation_id='expert_periodical_list',
        responses={200: PeriodicalListSerializer(many=True)}, tags=['periodicals']
    )
    def get(self, request, expert_id, *args, **kwargs):
        """
        查看某专家的期刊，
        路径参数 expert_id
        排序参数 order
        """
        order = request.query_params.get('order')
        queryset = Periodical.filter_by_expert_id(expert_id)
        if queryset:
            if order:
                queryset = queryset.order_by(order)
            data = get_results(request, queryset, self, PeriodicalListSerializer)
            return Response({'count': queryset.count(), 'periodicals': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is no such expert'}, status.HTTP_404_NOT_FOUND)


class PeriodicalView(generics.RetrieveAPIView):
    queryset = Periodical.objects.all()
    serializer_class = PeriodicalDetailSerializer

    @swagger_auto_schema(
        operation_id='periodical_read', responses={200: PeriodicalDetailSerializer()}, tags=['periodicals']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
