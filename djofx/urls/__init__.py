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
        r'^categories/$',
        views.category_list,
        name="djofx_categories"
    ),
    url(
        r'^categories/add/$',
        views.category_add,
        name="djofx_category_add"
    ),
    url(
        r'^categories/(?P<pk>\d+)/$',
        views.category_detail,
        name="djofx_category"
    ),
    url(
        r'^categories/(?P<pk>\d+)/edit/$',
        views.category_edit,
        name="djofx_category_edit"
    ),
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
