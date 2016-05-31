"""epulsa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt import views as jwtviews
from transaction import views
from users.views import TokenCreator

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^user/', include('users.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^transaction/', include('transaction.urls')),
    url(r'^api-auth/$', jwtviews.obtain_jwt_token),
    url(r'^api-auth2/$', TokenCreator.as_view()),
]
