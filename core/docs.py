from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from common.users import IsAdminUser

api_schema_view = get_schema_view(
    info=openapi.Info(
        title="Science Data API",
        default_version="v1.0",
        description="科搜搜",
        license=openapi.License(name="MIT License"),
    ),
    url="http://localhost:7501/api/",
    public=True,
    permission_classes=(IsAdminUser,),
)

admin_schema_view = get_schema_view(
    info=openapi.Info(
        title="Science Data API",
        default_version="v1.0",
        description="科搜搜",
        license=openapi.License(name="MIT License"),
    ),
    url="http://localhost:7501/admin/",
    public=True,
    permission_classes=(IsAdminUser,),
)
