# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from model.models import Expert
from api.serializers.expert import ExpertListSerializer, ExpertDetailSerializer
from common.page import get_results


class ExpertListView(APIView):

    @swagger_auto_schema(
        operation_id='expert_list', responses={200: ExpertListSerializer(many=True)}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        queryset = Expert.objects.all()
        if request.query_params.get('text'):
            text = request.query_params.get('text')
            queryset = queryset.filter(
                Q(name=text) | Q(organization=text) | Q(major__contains=text) | Q(research_areas__contains=text)
            )
        elif request.query_params.get('keywords'):
            keywords = request.query_params.get('keywords')
            queryset = queryset.filter(Q(keywords__contains=keywords))
        data = get_results(request, queryset, self, ExpertListSerializer)
        return Response({'count': queryset.count(), 'experts': data}, status.HTTP_200_OK)


class ExpertDetailView(generics.RetrieveAPIView):
    serializer_class = ExpertDetailSerializer
    queryset = Expert.objects.all()

    @swagger_auto_schema(
        operation_id='expert_read', responses={200: ExpertDetailSerializer()}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
