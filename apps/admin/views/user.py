import datetime

from django.db.models import Q
from django.contrib.auth.views import get_user_model
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from drf_yasg.utils import swagger_auto_schema

from common.users import authenticate, IsAdminUser
from common.page import page_params, get_results
from admin.parameters.user import create_token_response, create_token_body, token_parameters
from admin.parameters.user import user_create_parameters, user_update_parameters, user_filter_params
from admin.serializers.user import UserSerializer

User = get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UserJWTView(APIView):
    @swagger_auto_schema(
        request_body=create_token_body, operation_id='create_token', responses={201: create_token_response},
        tags=['users']
    )
    def post(self, request, *args, **kwargs):
        """
        登录
        """
        user = authenticate(request.data.get('username'), request.data.get('password'))
        if user:
            token = jwt_encode_handler(jwt_payload_handler(user))
            response = Response({'token': token, 'user_id': user.id}, status=status.HTTP_201_CREATED)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response
        return Response({'detail': '该用户校验不通过'}, status=status.HTTP_400_BAD_REQUEST)


class UsersView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]

    dic = {
        'false': False,
        'true': True
    }

    @swagger_auto_schema(
        manual_parameters=page_params + token_parameters + user_filter_params, operation_id='user_list',
        responses={200: UserSerializer(many=True)}, tags=['users']
    )
    def get(self, request, *args, **kwargs):
        """
        查看用户列表，
        查询参数 text, is_superuser, is_active，排序参数 order
        查询字段包括 name, mobile, email
        """
        text = request.query_params.get('text')
        is_superuser = request.query_params.get('is_superuser')
        is_active = request.query_params.get('is_active')
        order = request.query_params.get('order')
        queryset = User.objects.all()
        if text:
            queryset = queryset.filter(Q(name=text) | Q(mobile=text) | Q(email=text))
        if is_superuser:
            queryset = queryset.filter(is_superuser=self.dic[is_superuser])
        if is_active:
            queryset = queryset.filter(is_active=self.dic[is_active])
        if order:
            queryset = queryset.order_by(order)
        data = get_results(request, queryset, self, UserSerializer)
        return Response({'count': queryset.count(), 'users': data}, status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=user_create_parameters, operation_id='user_create',
        responses={201: UserSerializer()},
        tags=['users']
    )
    def post(self, request, *args, **kwargs):
        """
        创建用户
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data}, status.HTTP_201_CREATED)
        else:
            return Response({'error': f'{serializer.errors}'}, status.HTTP_400_BAD_REQUEST)


class UserView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        manual_parameters=token_parameters, operation_id='user_retrieve',
        responses={200: UserSerializer()}, tags=['users']
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=user_update_parameters, operation_id='user_update',
        responses={201: UserSerializer()}, tags=['users']
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=token_parameters, request_body=user_update_parameters, operation_id='user_partial_update',
        responses={201: UserSerializer()}, tags=['users']
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
