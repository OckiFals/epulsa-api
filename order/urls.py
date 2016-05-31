from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from order import views

urlpatterns = [
    url(r'^$', views.OrderList.as_view(), name="order-all"),
    url(r'^(?P<pk>[0-9]+)/$', views.OrderDetail.as_view(), name="order-detail"),
    # counter
    url(r'^streams/$', views.OrderStream.as_view(), name="order-streams"),
    url(r'^counter-turn/$', views.CounterTurn.as_view(), name="counter-turn"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
