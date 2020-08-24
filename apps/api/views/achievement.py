# -*- encoding=utf-8 -*-

from django.db.models import Q
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results
from common.order import order_params
from model.models import Expert, Achievement
from api.parameters.achievement import achievement_filter_params
from api.serializers.achievement import AchievementListSerializer, AchievementDetailSerializer


class AchievementsView(APIView):
    @swagger_auto_schema(
        manual_parameters=achievement_filter_params + order_params, operation_id='achievement_list',
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
    @swagger_auto_schema(
        manual_parameters=order_params, operation_id='expert_achievement_list',
        responses={200: AchievementListSerializer(many=True)}, tags=['achievements']
    )
    def get(self, request, pk, *args, **kwargs):
        order = request.query_params.get('order')
        expert = Expert.objects.filter(id=pk)
        if expert:
            queryset = expert.achievements
            if order:
                queryset = queryset.order_by(order)
            data = get_results(request, queryset, self, AchievementListSerializer)
            return Response({'count': queryset.count(), 'achievements': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is nos such expert'}, status.HTTP_404_NOT_FOUND)


class AchievementView(generics.RetrieveAPIView):
    serializer_class = AchievementDetailSerializer
    queryset = Achievement.objects.all()

    @swagger_auto_schema(
        operation_id='achievement_read', responses={200: AchievementDetailSerializer()}, tags=['achievements']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
