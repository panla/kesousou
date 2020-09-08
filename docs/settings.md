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
        terms_of_service="http://localhost:8201/api/",
    ),
    url="http://localhost:8201/api/",
    public=True,
    permission_classes=(IsAdminUser,),
)

admin_schema_view = get_schema_view(
    info=openapi.Info(
        title="Science Data API",
        default_version="v1.0",
        description="练习文档",
        terms_of_service="http://localhost:8201/admin/",
    ),
    url="http://localhost:8201/admin/",
    public=True,
    permission_classes=(IsAdminUser,),
)
```

```text
运行 python manage.py runserver localhost:7501
访问 localhost:8201/admin/doc/
访问 localhost:8201/api/doc/
```

## nginx

> 注意 nginx 权限问题

```text
server {
    listen      8201;
    server_name localhost;
    charset     UTF-8;
    client_max_body_size    75M;
    #charset koi8-r;

    access_log  /tmp/logs/kesousou/access.log;
    error_log   /tmp/logs/kesousou/error.log;
    location / {
        proxy_pass  http://localhost:8200;
        proxy_set_header    Host $http_host;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias   /xx/xxx/static;
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
        # 'HOST': '127.0.0.1',
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

## SECRET_KEY

生成 SECRET_KEY

```python
from django.core.management import utils

print(utils.get_random_secret_key())
```

## 静态文件

`core/local/settings.py`

```text
# 是否显示 swagger 文档
DISPLAY_DOCS = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOR = os.path.join(BASE_DIR, 'upload')

DEBUG = True/False

ALLOWED_HOSTS = []/['*']
```
