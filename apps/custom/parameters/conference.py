from drf_yasg import openapi

conference_filter_params = [
    openapi.Parameter(
        name='text', in_=openapi.IN_QUERY,
        description='title or first_creator or keywords',
        type=openapi.TYPE_STRING
    ),
]
