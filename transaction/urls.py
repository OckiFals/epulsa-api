from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from transaction import views

urlpatterns = [
    url(r'^counter$', views.TransactionListCounter.as_view(), name="transaction-counter-all"),
    url(r'^(?P<pk>[0-9]+)/$', views.TransactionListCounter.as_view(), name="order-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
