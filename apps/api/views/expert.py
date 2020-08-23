# -*- encoding=utf-8 -*-

from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

from model.models import Expert
from api.serializers.expert import ExpertListSerializer, ExpertDetailSerializer
from common.page import PagePagination


class ExpertListView(generics.ListAPIView):
    serializer_class = ExpertListSerializer
    pagination_class = PagePagination
    queryset = Expert.objects.all()

    @swagger_auto_schema(
        operation_id='expert_list', responses={200: ExpertListSerializer(many=True)}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ExpertDetailView(generics.RetrieveAPIView):
    serializer_class = ExpertDetailSerializer
    queryset = Expert.objects.all()

    @swagger_auto_schema(
        operation_id='expert_read', responses={200: ExpertDetailSerializer()}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
