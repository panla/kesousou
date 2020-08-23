# -*- encoding=utf-8 -*-

from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from model.models import Expert, Conferences
from api.serializers.conference import ConferenceListSerializer, ConferenceDetailSerializer
from common.page import PagePagination


class ConferenceListView(generics.ListAPIView):
    serializer_class = ConferenceListSerializer
    queryset = Conferences.objects.all()
    pagination_class = PagePagination

    @swagger_auto_schema(
        operation_id='conference_list', responses={200: ConferenceListSerializer(many=True)}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ConferenceDetailView(generics.RetrieveAPIView):
    serializer_class = ConferenceListSerializer
    queryset = Conferences.objects.all()

    @swagger_auto_schema(
        operation_id='conference_read', responses={200: ConferenceDetailSerializer()}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
