# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results
from model.models import Expert
from api.parameters.expert import expert_filter_params
from api.serializers.expert import ExpertListSerializer, ExpertDetailSerializer


class ExpertListView(APIView):

    @swagger_auto_schema(
        manual_parameters=expert_filter_params,
        operation_id='expert_list', responses={200: ExpertListSerializer(many=True)}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text')
        queryset = Expert.objects.all()
        if text:
            queryset = queryset.filter(
                Q(name=text) | Q(organization=text) | Q(major__contains=text) | Q(research_areas__contains=text)
                | Q(personal_introduction__contains=text | Q(keywords__contains=text))
            )
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
