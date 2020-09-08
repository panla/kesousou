"""
排序参数，
id 根据 id 来升序
-id 根据 id 来降序
"""

from drf_yasg import openapi

order_param = openapi.Parameter(
    name='order', in_=openapi.IN_QUERY,
    description='order by', type=openapi.TYPE_STRING
)

order_params = [
    order_param
]
