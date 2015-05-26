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
]
