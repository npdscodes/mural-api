"""mural_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from .routers import router

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_swagger.views import get_swagger_view

from accounts.viewsets import SignUpView


schema_view = get_swagger_view(title='MURAL API')

urlpatterns = [
    url(r'^api/v1/token/$', obtain_auth_token, name='api-token'),
    url(r'^api/v1/signup/$', SignUpView.as_view(), name='signup'),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/docs/$', schema_view),
]
