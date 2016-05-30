from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
    # customer
    url(r'^customer/$', views.CustomerList.as_view(), name="customer-all"),
    url(r'^customer/(?P<pk>[0-9]+)/$', views.CustomerDetail.as_view(), name="customer-detail"),
    # counter
    url(r'^counter/$', views.CounterList.as_view(), name="counter-all"),
    url(r'^counter/(?P<pk>[0-9]+)/$', views.CounterDetail.as_view(), name="counter-detail"),
    # admin
    url(r'^admin/$', views.AdminList.as_view(), name="admin-all"),
    url(r'^admin/(?P<pk>[0-9]+)/$', views.AdminDetail.as_view(), name="admin-detail"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
