from django.conf.urls import url
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
    url(
        r'^account/(?P<pk>\d+)/auto/$',
        views.account_auto_categorise,
        name="djofx_account_autocategorise"
    ),
    url(
        r'^category/add/$',
        views.add_category,
        name="djofx_category_add"
    ),
    url(
        r'^category/(?P<pk>\d+)/$',
        views.category_detail,
        name="djofx_category"
    ),
    url(
        r'^categorise/(?P<pk>\d+)/',
        views.categorise,
        name="djofx_categorise"
    ),
    url(
        r'^transaction/(?P<pk>\d+)/verify/',
        views.transaction_mark_verified,
        name="djofx_transaction_verify"
    ),
    url(
        r'^transaction/(?P<pk>\d+)/reguess/',
        views.transaction_reguess,
        name="djofx_transaction_reguess"
    ),
    url(r'^accuracy/', views.accuracy, name="djofx_accuracy"),
    url(
        r'^monthly/$',
        views.monthly_breakdown,
        name="djofx_monthly"
    ),
]
