# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results
from model.models import Expert, Patent
from api.serializers.patent import PatentListSerializer, PatentDetailSerializer
from api.parameters.patent import patent_filter_params


class PatentsView(APIView):
    @swagger_auto_schema(
        manual_parameters=patent_filter_params,
        operation_id='patent_list', responses={200: PatentListSerializer(many=True)}, tags=['patents']
    )
    def get(self, request, *args, **kwargs):
        queryset = Patent.objects.all()
        if request.data.get('text'):
            text = request.query_params.get('text')
            queryset = queryset.filter(
                Q(patent_code=text) | Q(publication_number=text) | Q(name__contains=text) | Q(abstract__contains=text)
                | Q(inventors__contains=text)
            )
        data = get_results(request, queryset, self, PatentListSerializer)
        return Response({'count': queryset.count(), 'patents': data}, status.HTTP_200_OK)


class ExpertPatentsView(APIView):
    @swagger_auto_schema(
        operation_id='expert_patent_list', responses={200: PatentListSerializer(many=True)}, tags=['patents']
    )
    def get(self, request, pk, *args, **kwargs):
        expert = Expert.objects.filter(id=pk).first()
        if expert:
            queryset = expert.patents
            data = get_results(request, queryset, self, PatentListSerializer)
            return Response({'count': queryset.count(), 'patents': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is no such expert'}, status.HTTP_404_NOT_FOUND)


class PatentView(generics.RetrieveAPIView):
    @swagger_auto_schema(
        operation_id='patent_read', responses={200: PatentDetailSerializer()}, tags=['patents']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
