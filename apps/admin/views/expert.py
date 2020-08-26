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
from model.models import Expert
from admin.parameters.user import token_parameters
from admin.parameters.expert import expert_filter_params, expert_create_params, expert_update_params
from admin.serializers.expert import ExpertListSerializer, ExpertDetailSerializer


class ExpertsView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=expert_filter_params + order_params + page_params, operation_id='expert_list',
        responses={200: ExpertListSerializer(many=True)}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text')
        order = request.query_params.get('order')
        queryset = Expert.objects.all()
        if text:
            queryset = queryset.filter(
                Q(name=text) | Q(organization=text) | Q(major__contains=text) | Q(research_areas__contains=text)
                | Q(keywords__contains=text)
            )
        if order:
            queryset = queryset.order_by(order)
        data = get_results(request, queryset, self, ExpertListSerializer)
        return Response({'count': queryset.count(), 'experts': data}, status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=expert_create_params, operation_id='expert_create',
        responses={201: ExpertDetailSerializer()}, tags=['experts']
    )
    def post(self, request, *args, **kwargs):
        serializer = ExpertDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'expert': serializer.data}, status.HTTP_201_CREATED)
        else:
            return Response({'error': f'{serializer.errors}'}, status.HTTP_400_BAD_REQUEST)


class ExpertView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ExpertDetailSerializer
    queryset = Expert.objects.all()

    @swagger_auto_schema(
        operation_id='expert_read', responses={200: ExpertDetailSerializer()}, tags=['experts']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=expert_update_params, operation_id='expert_update',
        responses={201: ExpertDetailSerializer()}, tags=['experts']
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=expert_update_params, operation_id='expert_partial_update',
        responses={201: ExpertDetailSerializer()}, tags=['experts']
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
