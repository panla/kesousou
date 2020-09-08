from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class IndexView(APIView):
    @swagger_auto_schema(
        operation_id='index', tags=['index']
    )
    def get(self, request, *args, **kwargs):
        data = {'msg': 'this is index view'}
        return Response(data, status.HTTP_200_OK)
