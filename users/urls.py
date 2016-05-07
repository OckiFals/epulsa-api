from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
    url(r'^customer/$', views.CustomerList.as_view()),
    url(r'^customer/(?P<pk>[0-9]+)/$', views.CustomerDetail.as_view(), name="customer-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
