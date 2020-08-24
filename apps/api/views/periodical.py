# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results
from model.models import Expert, Periodical
from api.serializers.periodical import PeriodicalListSerializer, PeriodicalDetailSerializer
from api.parameters.periodical import periodical_filter_params


class PeriodicalsView(APIView):
    @swagger_auto_schema(
        manual_parameters=periodical_filter_params,
        operation_id='periodical_list', responses={200: PeriodicalListSerializer(many=True)}, tags=['periodicals']
    )
    def get(self, request, *args, **kwargs):
        queryset = Periodical.objects.all()
        text = request.query_params.get('text')
        if text:
            queryset = queryset.filter(
                Q(doi=text) | Q(title__contains=text) | Q(first_creator=text) | Q(periodical_name=text)
                | Q(foundations__contains=text) | Q(keywords__contains=text) | Q(abstract__contains=text)
            )
        data = get_results(request, queryset, self, PeriodicalDetailSerializer)
        return Response({'count': queryset.count(), 'periodicals': data}, status.HTTP_200_OK)


class ExpertPeriodicalsView(APIView):
    @swagger_auto_schema(
        operation_id='expert_periodical_list', responses={200: PeriodicalListSerializer(many=True)},
        tags=['periodicals']
    )
    def get(self, request, pk, *args, **kwargs):
        expert = Expert.objects.filter(id=pk).first()
        if expert:
            queryset = expert.periodicals
            data = get_results(request, queryset, self, PeriodicalListSerializer)
            return Response({'count': queryset.count(), 'periodicals': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is no such expert'}, status.HTTP_404_NOT_FOUND)


class PeriodicalView(generics.RetrieveAPIView):
    @swagger_auto_schema(
        operation_id='periodical_read', responses={200: PeriodicalDetailSerializer()}, tags=['periodicals']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
