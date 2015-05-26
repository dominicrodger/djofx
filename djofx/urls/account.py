from django.conf.urls import url
from djofx import views


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.account_detail, name="djofx_account"),
    url(
        r'^(?P<pk>\d+)/unverified/$',
        views.account_detail,
        {'unverified': True},
        name="djofx_account_unverified"
    ),
]
