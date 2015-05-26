from django.conf.urls import url
from djofx import views

urlpatterns = [
    url(
        r'^(?P<pk>\d+)/categorise/$',
        views.transaction_categorise,
        name="djofx_categorise"
    ),
    url(
        r'^(?P<pk>\d+)/verify/$',
        views.transaction_mark_verified,
        name="djofx_transaction_verify"
    ),
    url(
        r'^list/(?P<type>([A-Za-z0-9]+))/(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.transaction_list,
        name="djofx_transaction_list"
    ),

]
