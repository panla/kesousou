# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results
from model.models import Expert, Conferences
from api.parameters.conference import conference_filter_params
from api.serializers.conference import ConferenceListSerializer, ConferenceDetailSerializer


class ConferencesView(APIView):
    @swagger_auto_schema(
        manual_parameters=conference_filter_params,
        operation_id='conference_list', responses={200: ConferenceListSerializer(many=True)}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text')
        queryset = Conferences.objects.all()
        if text:
            queryset = queryset.filter(
                Q(title__contains=text) | Q(abstract__contains=text) | Q(first_creator=text)
                | Q(meeting_title__contains=text) | Q(keywords__contains=text)
            )
        data = get_results(request, queryset, self, ConferenceListSerializer)
        return Response({'count': queryset.count(), 'conferences': data}, status.HTTP_200_OK)


class ExpertConferencesView(APIView):
    @swagger_auto_schema(
        operation_id='expert_conference_list', responses={200: ConferenceListSerializer(many=True)},
        tags=['conferences']
    )
    def get(self, request, pk, *args, **kwargs):
        expert = Expert.objects.filter(id=pk).first()
        if expert:
            queryset = expert.conferences
            data = get_results(request, queryset, self, ConferenceListSerializer)
            return Response({'count': queryset.count(), 'conferences': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is no such expert'}, status.HTTP_404_NOT_FOUND)


class ConferenceView(generics.RetrieveAPIView):
    serializer_class = ConferenceListSerializer
    queryset = Conferences.objects.all()

    @swagger_auto_schema(
        operation_id='conference_read', responses={200: ConferenceDetailSerializer()}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
