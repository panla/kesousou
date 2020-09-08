from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from common.page import get_results, page_params
from common.order import order_params
from common.users import IsAdminUser
from model.models import Expert, Patent
from admin.parameters.user import token_parameters
from admin.parameters.patent import patent_filter_params, patent_update_params
from admin.serializers.patent import PatentListSerializer, PatentDetailSerializer


class PatentsView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=patent_filter_params + order_params + page_params + token_parameters,
        operation_id='patent_list', responses={200: PatentListSerializer(many=True)}, tags=['patents']
    )
    def get(self, request, *args, **kwargs):
        """
        查看专利列表，
        查询参数 text，排序参数 order
        模糊查询字段包括 name, inventors
        精准查询字段包括 patent_code, publication_number
        """
        text = request.query_params.get('text')
        order = request.query_params.get('order')
        queryset = Patent.objects.all()
        if text:
            queryset = queryset.filter(
                Q(patent_code=text) | Q(publication_number=text) | Q(name__contains=text) | Q(inventors__contains=text)
            )
        if order:
            queryset = queryset.order_by(order_params)
        data = get_results(request, queryset, self, PatentListSerializer)
        return Response({'count': queryset.count(), 'patents': data}, status.HTTP_200_OK)


class ExpertPatentsView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=order_params + page_params + token_parameters, operation_id='expert_patent_list',
        responses={200: PatentListSerializer(many=True)}, tags=['patents']
    )
    def get(self, request, expert_id, *args, **kwargs):
         """
        查看某专家的专利，
        路径参数 expert_id
        排序参数 order
        """
        order = request.query_params.get('order')
        expert = Expert.objects.filter(id=expert_id).first()
        if expert:
            queryset = expert.patents
            if order:
                queryset = queryset.order_by(order_params)
            data = get_results(request, queryset, self, PatentListSerializer)
            return Response({'count': queryset.count(), 'patents': data}, status.HTTP_200_OK)
        else:
            return Response({'error': 'there is no such expert'}, status.HTTP_404_NOT_FOUND)


class PatentView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Patent.objects.all()
    serializer_class = PatentDetailSerializer

    @swagger_auto_schema(
        manual_parameters=token_parameters, operation_id='patent_read', responses={200: PatentDetailSerializer()},
        tags=['patents']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=patent_update_params, operation_id='patent_update',
        responses={201: PatentDetailSerializer()}, tags=['patents']
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=patent_update_params, operation_id='patent_partial_update',
        responses={201: PatentDetailSerializer()}, tags=['patents']
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
