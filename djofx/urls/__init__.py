from django.conf.urls import include, url
from djofx import views

urlpatterns = [
    url(r'^$', views.home_page, name="djofx_home"),
    url(r'^upload/', views.upload_ofx_file, name="djofx_upload"),
    url(r'^account/(?P<pk>\d+)/$', views.account_detail, name="djofx_account"),
    url(
        r'^account/(?P<pk>\d+)/unverified/$',
        views.account_detail,
        {'unverified': True},
        name="djofx_account_unverified"
    ),
    url(r'^categories/', include('djofx.urls.categories')),
    url(
        r'^transaction/(?P<pk>\d+)/categorise/',
        views.transaction_categorise,
        name="djofx_categorise"
    ),
    url(
        r'^transaction/(?P<pk>\d+)/verify/',
        views.transaction_mark_verified,
        name="djofx_transaction_verify"
    ),
    url(
        r'^monthly/$',
        views.monthly_breakdown,
        name="djofx_monthly"
    ),
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
]
