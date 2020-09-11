"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from custom.views.index import IndexView

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'accounts/profile/$', IndexView.as_view()),
    path('auth/login/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', include('admin.urls', namespace='admin')),
    path('custom/', include('custom.urls', namespace='custom')),
]
