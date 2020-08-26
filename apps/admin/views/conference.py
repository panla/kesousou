# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results, page_params
from common.order import order_params
from common.users import IsAdminUser
from model.models import Expert, Conference
from admin.parameters.user import token_parameters
from admin.parameters.conference import conference_filter_params, conference_update_params
from admin.serializers.conference import ConferenceListSerializer, ConferenceDetailSerializer


class ConferencesView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=conference_filter_params + order_params + page_params + token_parameters,
        operation_id='conference_list', responses={200: ConferenceListSerializer(many=True)}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
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
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=order_params + page_params + token_parameters, operation_id='expert_conference_list',
        responses={200: ConferenceListSerializer(many=True)}, tags=['conferences']
    )
    def get(self, request, expert_id, *args, **kwargs):
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


class ConferenceView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ConferenceListSerializer
    queryset = Conference.objects.all()

    @swagger_auto_schema(
        manual_parameters=token_parameters, operation_id='conference_read',
        responses={200: ConferenceDetailSerializer()}, tags=['conferences']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=conference_update_params, operation_id='conference_update',
        responses={201: ConferenceDetailSerializer()}, tags=['conferences']
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=conference_update_params,
        operation_id='conference_partial_update', responses={201: ConferenceDetailSerializer()}, tags=['conferences']
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
