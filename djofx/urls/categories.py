from django.conf.urls import url
from djofx.views import (
    category_add,
    category_detail,
    category_edit,
    category_list
)

urlpatterns = [
    url(r'^$', category_list, name="djofx_categories"),
    url(r'^add/$', category_add, name="djofx_category_add"),
    url(r'^(?P<pk>\d+)/$', category_detail, name="djofx_category"),
    url(r'^(?P<pk>\d+)/edit/$', category_edit, name="djofx_category_edit"),
]
