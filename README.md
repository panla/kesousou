# 科搜搜系统

## 环境

Python==3.8.3

```bash
pip install docs/requirements.txt
```

配置

```text
# swagger 配置
# 在 core/local/docs.py

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from common.users import IsAdminUser

api_schema_view = get_schema_view(
    info=openapi.Info(
        title="Science Data API",
        default_version="v1.0",
        description="练习文档",
        terms_of_service="http://localhost:7501/api/",
    ),
    url="http://localhost:7501/api/",
    public=True,
    permission_classes=(IsAdminUser,),
)

admin_schema_view = get_schema_view(
    info=openapi.Info(
        title="Science Data API",
        default_version="v1.0",
        description="练习文档",
        terms_of_service="http://localhost:7501/admin/",
    ),
    url="http://localhost:7501/admin/",
    public=True,
    permission_classes=(IsAdminUser,),
)
```

```text
运行 python manage.py runserver localhost:7501
访问 localhost:7501/admin/doc/
访问 localhost:7501/api/doc/
```

## 介绍

> 这个小系统是利用Python Django DRF 等开发的一套搜科技数据的工具
> 包括搜专家，搜专利，搜期刊，搜会议，搜成果