# 配置

## `drf_yasg` swagger 文档配置

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

## nginx

```text
server {
    listen      7501;
    server_name localhost;
    charset     UTF-8;
    client_max_body_size    75M;
    #charset koi8-r;

    access_log  /tmp/logs/kesousou/access.log;
    error_log   /tmp/logs/kesousou/error.log;
    location / {
        proxy_pass  http://localhost:7500;
        proxy_set_header    Host $http_host;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias   /xx/xxx/static/;
    }
}
```

## database

```text
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'experts',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'password',
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'NAME': 'test_experts'
        }
    }
}
```
