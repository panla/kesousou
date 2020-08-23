# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from model.models import Expert, Patent
from api.serializers.patent import PatentListSerializer, PatentDetailSerializer
from common.page import get_results


class PatentListView(APIView):
    @swagger_auto_schema(
        operation_id='patent_list', responses={200: PatentListSerializer(many=True)}, tags=['patents']
    )
    def get(self, request, *args, **kwargs):
        queryset = Patent.objects.all()
        if request.query_params.get('text'):
            text = request.query_params.get('text')
            queryset = queryset.filter(
                Q(name__contains=text) | Q(name=text) | Q(abstract__contains=text)
            )
        elif request.query_params.get('code'):
            code = request.query_params.get('code')
            queryset = queryset.filter(Q(patent_code=code) | Q(publication_number=code))
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


class PatentDetailView(generics.RetrieveAPIView):
    @swagger_auto_schema(
        operation_id='patent_read', responses={200: PatentDetailSerializer()}, tags=['patents']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
