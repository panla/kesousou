from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results, page_params
from common.order import order_params
from model.models import Expert, Conference
from custom.parameters.conference import conference_filter_params
from custom.serializers.conference import ConferenceListSerializer, ConferenceDetailSerializer


class ConferencesView(APIView):
    @swagger_auto_schema(
        manual_parameters=conference_filter_params + order_params + page_params, operation_id='conference_list',
        responses={200: ConferenceListSerializer(many=True)}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
        """
        查看会议列表，
        查询参数 text，排序参数 order
        模糊查询字段包括 title, keywords
        精准查询字段包括 first_creator
        """
        text = request.query_params.get('text')
        order = request.query_params.get('order')
        queryset = Conference.objects.all()
        if text:
            queryset = queryset.filter(
                Q(title__contains=text) | Q(first_creator=text) | Q(keywords__contains=text)
            )
        if order:
            queryset = queryset.order_by(order)
        data = get_results(request, queryset, self, ConferenceListSerializer)
        return Response({'count': queryset.count(), 'conferences': data}, status.HTTP_200_OK)


class ExpertConferencesView(APIView):
    @swagger_auto_schema(
        manual_parameters=order_params + page_params, operation_id='expert_conference_list',
        responses={200: ConferenceListSerializer(many=True)}, tags=['conferences']
    )
    def get(self, request, expert_id, *args, **kwargs):
        """
        查看某专家的会议列表，
        路径参数 expert_id，排序参数 order
        """
        order = request.query_params.get('order')
        expert = Expert.objects.filter(id=expert_id).first()
        if expert:
            queryset = expert.conferences.all()
            if order:
                queryset = queryset.order_by(order)
            data = get_results(request, queryset, self, ConferenceListSerializer)
            return Response({'count': queryset.count(), 'conferences': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is no such expert'}, status.HTTP_404_NOT_FOUND)


class ConferenceView(generics.RetrieveAPIView):
    serializer_class = ConferenceListSerializer
    queryset = Conference.objects.all()

    @swagger_auto_schema(
        operation_id='conference_read', responses={200: ConferenceDetailSerializer()}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
