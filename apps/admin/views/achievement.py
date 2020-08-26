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
from model.models import Expert, Achievement
from admin.parameters.user import token_parameters
from admin.parameters.achievement import achievement_filter_params, achievement_update_params
from admin.serializers.achievement import AchievementListSerializer, AchievementDetailSerializer


class AchievementsView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]

    @swagger_auto_schema(
        manual_parameters=achievement_filter_params + order_params + page_params + token_parameters,
        operation_id='achievement_list',
        responses={200: AchievementListSerializer(many=True)}, tags=['achievements']
    )
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text')
        order = request.query_params.get('order')
        queryset = Achievement.objects.all()
        if text:
            queryset = queryset.filter(
                Q(sn=text) | Q(title__contains=text) | Q(keywords__contains=text) | Q(organizations__contains=text)
                | Q(creators__contains=text)
            )
        if order:
            queryset = queryset.order_by(order)
        data = get_results(request, queryset, self, AchievementListSerializer)
        return Response({'count': queryset.count(), 'achievements': data}, status.HTTP_200_OK)


class ExpertAchievementsView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]

    @swagger_auto_schema(
        manual_parameters=order_params + page_params + token_parameters, operation_id='expert_achievement_list',
        responses={200: AchievementListSerializer(many=True)}, tags=['achievements']
    )
    def get(self, request, expert_id, *args, **kwargs):
        order = request.query_params.get('order')
        expert = Expert.objects.filter(id=expert_id).first()
        if expert:
            queryset = expert.achievements.all()
            if order:
                queryset = queryset.order_by(order)
            data = get_results(request, queryset, self, AchievementListSerializer)
            return Response({'count': queryset.count(), 'achievements': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is nos such expert'}, status.HTTP_404_NOT_FOUND)


class AchievementView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = AchievementDetailSerializer
    queryset = Achievement.objects.all()

    @swagger_auto_schema(
        manual_parameters=token_parameters, operation_id='achievement_read',
        responses={200: AchievementDetailSerializer()}, tags=['achievements']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=achievement_update_params, operation_id='achievement_update',
        responses={201: AchievementDetailSerializer()}, tags=['achievements']
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=achievement_update_params,
        operation_id='achievement_partial_update', responses={201: AchievementDetailSerializer()}, tags=['achievements']
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
