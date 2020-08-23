# -*- encoding=utf-8 -*-

import datetime

from django.contrib.auth.views import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

from admin.parameters.user import create_token_response, create_token_body
from common.users import authenticate

User = get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UserJWTView(APIView):
    @swagger_auto_schema(request_body=create_token_body, responses={201: create_token_response})
    def post(self, request, *args, **kwargs):
        user = authenticate(request.data.get('username'), request.data.get('password'))
        if user:
            token = jwt_encode_handler(jwt_payload_handler(user))
            response = Response({'token': token, 'user_id': user.id}, status=status.HTTP_201_CREATED)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True)
            return response
        return Response({'detail': '该用户校验不通过'}, status=status.HTTP_400_BAD_REQUEST)
