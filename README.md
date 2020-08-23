# 科搜搜系统

## 环境

Python==3.8.3

```bash
pip install docs/requirements.txt
```

配置

```python
# swagger 配置
# 在 core/local/docs.py

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from common.users import IsAdminUser

schema_view = get_schema_view(
    info=openapi.Info(
        title="Science Data API",
        default_version='v1.0',
        description="练习文档",
        terms_of_service="http://localhost:7101",
        contact=openapi.Contact(email="admin@sys.com"),
        license=openapi.License(name="BSD License"),
    ),
    url="http://localhost:7101",
    public=True,
    permission_classes=(IsAdminUser,),
)

```

## 介绍

> 这个小系统是利用Python Django DRF 等开发的一套搜科技数据的工具
> 包括搜专家，搜专利，搜期刊，搜会议，搜成果